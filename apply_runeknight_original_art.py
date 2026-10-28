#!/usr/bin/env python3
"""Apply ORIGINAL Rune Knight character art / subclass art / class armor / talent tree.
Run this AFTER apply_runeknight_v402.py on upstream Shattered PD 4.0.2.
The generated images are produced by make_runeknight_assets.py (Pillow).
Copyright (C) 2026 community mod contributors, GPL-3.0-or-later.
"""
import sys, shutil
from pathlib import Path
from PIL import Image

root=Path(sys.argv[1]).resolve()
assets=Path(sys.argv[2] if len(sys.argv)>2 else '/mnt/data/runeknight-original-assets').resolve()
code=Path('core/src/main/java/com/shatteredpixel/shatteredpixeldungeon')

def rep(path,old,new,expected=1):
    file=root/path
    s=file.read_text('utf-8')
    actual=s.count(old)
    if actual!=expected:raise RuntimeError(f'Anchor mismatch in {path}: expected {expected}, got {actual}: {old[:125]!r}')
    file.write_text(s.replace(old,new,expected),encoding='utf-8')
    print('PATCH',path)

def append(path,text):
    f=root/path
    with f.open('a',encoding='utf-8') as o:o.write('\n'+text.strip()+'\n')

hero=code/'actors/hero/HeroClass.java'
rep(hero,'RUNEKNIGHT( HeroSubClass.BERSERKER, HeroSubClass.GLADIATOR );','RUNEKNIGHT( HeroSubClass.RUNE_SENTINEL, HeroSubClass.RUNE_REAVER );')
rep(hero,'\t\t\tcase CLERIC:\n\t\t\t\treturn Assets.Sprites.CLERIC;', '\t\t\tcase CLERIC:\n\t\t\t\treturn Assets.Sprites.CLERIC;\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\treturn Assets.Sprites.RUNEKNIGHT;')
rep(hero,'\t\t\tcase CLERIC:\n\t\t\t\treturn Assets.Splashes.CLERIC;', '\t\t\tcase CLERIC:\n\t\t\t\treturn Assets.Splashes.CLERIC;\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\treturn Assets.Splashes.RUNEKNIGHT;')
rep(hero,'\t\t\tcase CLERIC:\n\t\t\t\treturn new ArmorAbility[]{new AscendedForm(), new Trinity(), new PowerOfMany()};', '\t\t\tcase CLERIC:\n\t\t\t\treturn new ArmorAbility[]{new AscendedForm(), new Trinity(), new PowerOfMany()};\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\treturn new ArmorAbility[]{new HeroicLeap(), new Shockwave(), new Endure()};')

sub=code/'actors/hero/HeroSubClass.java'
rep(sub,'\tPALADIN(HeroIcon.PALADIN);','\tPALADIN(HeroIcon.PALADIN),\n\n\tRUNE_SENTINEL(HeroIcon.RUNE_SENTINEL),\n\tRUNE_REAVER(HeroIcon.RUNE_REAVER);')

armor=code/'items/armor/ClassArmor.java'
rep(armor,'\t\t\tcase WARRIOR:\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\tclassArmor = new WarriorArmor();', '\t\t\tcase WARRIOR:\n\t\t\t\tclassArmor = new WarriorArmor();\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\tclassArmor = new RuneKnightArmor();')
(r:=root/code/'items/armor/RuneKnightArmor.java').write_text('''/* Rune Knight original armor icon; GPL-3.0-or-later. */
package com.shatteredpixel.shatteredpixeldungeon.items.armor;
import com.shatteredpixel.shatteredpixeldungeon.sprites.ItemSpriteSheet;
public class RuneKnightArmor extends ClassArmor {
    { image = ItemSpriteSheet.RUNEKNIGHT_ARMOR; }
}
''',encoding='utf-8')

ass=code/'Assets.java'
rep(ass,'public static final String TALENT_ICONS     = "interfaces/talent_icons.png";', '''public static final String TALENT_ICONS     = "interfaces/talent_icons.png";
        public static final String RUNEKNIGHT_TALENTS = "interfaces/runeknight_talents.png";
        public static final String RUNEKNIGHT_SUBCLASSES = "interfaces/runeknight_subclasses.png";
        public static final String RUNEKNIGHT_ABILITIES = "interfaces/runeknight_abilities.png";''')
rep(ass,'public static final String CLERIC   = "splashes/cleric.jpg";', '''public static final String CLERIC   = "splashes/cleric.jpg";
        public static final String RUNEKNIGHT = "splashes/runeknight.jpg";''')
rep(ass,'public static final String CLERIC   = "sprites/cleric.png";', '''public static final String CLERIC   = "sprites/cleric.png";
        public static final String RUNEKNIGHT = "sprites/runeknight.png";''')

sheet=code/'sprites/ItemSpriteSheet.java'
rep(sheet,'public static final int DEWDROP         = UNCOLLECTIBLE+3;', '''public static final int RUNIC_FOCUS    = UNCOLLECTIBLE+2;
    public static final int RUNEKNIGHT_ARMOR = UNCOLLECTIBLE+7;
    public static final int DEWDROP         = UNCOLLECTIBLE+3;''')
rep(sheet,'\t\tassignItemRect(DEWDROP,     10,  9);', '''        assignItemRect(RUNIC_FOCUS, 16, 16);
        assignItemRect(RUNEKNIGHT_ARMOR, 16, 16);
\t\tassignItemRect(DEWDROP,     10,  9);''')
focus=code/'items/RunicFocus.java'
rep(focus,'image = ItemSpriteSheet.WAND_MAGIC_MISSILE;', 'image = ItemSpriteSheet.RUNIC_FOCUS;')
rep(focus,'5f + 2f * hero.pointsInTalent(Talent.RUNIC_MASTERY)', '''5f + 2f * hero.pointsInTalent(Talent.RUNIC_MASTERY)
                + hero.pointsInTalent(Talent.RUNIC_HEART)
                + hero.pointsInTalent(Talent.RUNIC_RESOLVE)
                + hero.pointsInTalent(Talent.RUNIC_FLOW)''')
rep(focus,'2 * hero.pointsInTalent(Talent.RUNIC_WARD)', '''2 * hero.pointsInTalent(Talent.RUNIC_WARD)
                    + 3 * hero.pointsInTalent(Talent.RUNIC_FORTRESS)
                    + 2 * hero.pointsInTalent(Talent.RUNIC_AEGIS)
                    + 2 * hero.pointsInTalent(Talent.RUNIC_OVERCHARGE)
                    + hero.pointsInTalent(Talent.RUNIC_TITAN)''')
# Shielding applied by subclass talents should work even without the T1 Rune Ward talent.
rep(focus,'if (hero.hasTalent(Talent.RUNIC_WARD)) {','''if (hero.hasTalent(Talent.RUNIC_WARD) || hero.hasTalent(Talent.RUNIC_FORTRESS)
                || hero.hasTalent(Talent.RUNIC_AEGIS) || hero.hasTalent(Talent.RUNIC_OVERCHARGE)
                || hero.hasTalent(Talent.RUNIC_TITAN)) {''')
rep(focus,'12f - 2f * hero.pointsInTalent(Talent.RUNIC_RECOVERY)', '''12f - 2f * hero.pointsInTalent(Talent.RUNIC_RECOVERY)
                - hero.pointsInTalent(Talent.RUNIC_BATTERY)
                - hero.pointsInTalent(Talent.RUNIC_RESOLVE)''')

talent=code/'actors/hero/Talent.java'
rep(talent,'RUNIC_EDGE(34), RUNIC_WARD(35), RUNIC_MASTERY(37), RUNIC_RECOVERY(39),', '''RUNIC_EDGE(34), RUNIC_WARD(35), RUNIC_MASTERY(37), RUNIC_RECOVERY(39),
    RUNIC_SPARK(240), RUNIC_BATTERY(241),
    RUNIC_ECHO(242), RUNIC_OVERCHARGE(243), RUNIC_HEART(244),
    RUNIC_TITAN(245, 3), RUNIC_MOMENTUM(246, 3),
    RUNIC_FORTRESS(247, 3), RUNIC_AEGIS(248, 3), RUNIC_RESOLVE(249, 3),
    RUNIC_FURY(250, 3), RUNIC_EXECUTION(251, 3), RUNIC_FLOW(252, 3),''')
rep(talent,'Collections.addAll(tierTalents, RUNIC_EDGE, RUNIC_WARD, PATIENT_STRIKE, AGGRESSIVE_BARRIER);', 'Collections.addAll(tierTalents, RUNIC_EDGE, RUNIC_WARD, RUNIC_SPARK, RUNIC_BATTERY);')
rep(talent,'Collections.addAll(tierTalents, RUNIC_MASTERY, RUNIC_RECOVERY, WEAPON_RECHARGING, LETHAL_HASTE, SWIFT_EQUIP);', 'Collections.addAll(tierTalents, RUNIC_MASTERY, RUNIC_RECOVERY, RUNIC_ECHO, RUNIC_OVERCHARGE, RUNIC_HEART);')
rep(talent,'\t\t\tcase RUNEKNIGHT:\n\t\t\t\tCollections.addAll(tierTalents, HOLD_FAST, STRONGMAN);', '\t\t\tcase RUNEKNIGHT:\n\t\t\t\tCollections.addAll(tierTalents, RUNIC_TITAN, RUNIC_MOMENTUM);')
rep(talent,'\t\t\tcase PALADIN:\n\t\t\t\tCollections.addAll(tierTalents, LAY_ON_HANDS, AURA_OF_PROTECTION, WALL_OF_LIGHT);\n\t\t\t\tbreak;', '''\t\t\tcase PALADIN:
\t\t\t\tCollections.addAll(tierTalents, LAY_ON_HANDS, AURA_OF_PROTECTION, WALL_OF_LIGHT);
\t\t\t\tbreak;
            case RUNE_SENTINEL:
                Collections.addAll(tierTalents, RUNIC_FORTRESS, RUNIC_AEGIS, RUNIC_RESOLVE);
                break;
            case RUNE_REAVER:
                Collections.addAll(tierTalents, RUNIC_FURY, RUNIC_EXECUTION, RUNIC_FLOW);
                break;''')
rep(talent,'dmg += 2 + hero.pointsInTalent(RUNIC_EDGE);', '''dmg += 2 + hero.pointsInTalent(RUNIC_EDGE)
                    + hero.pointsInTalent(RUNIC_SPARK)
                    + hero.pointsInTalent(RUNIC_ECHO)
                    + hero.pointsInTalent(RUNIC_MOMENTUM)
                    + hero.pointsInTalent(RUNIC_FURY);
            if (enemy.HP * 2 <= enemy.HT) {
                dmg += hero.pointsInTalent(RUNIC_EXECUTION);
            }''')
# Remove double semicolon introduced by replacing only the expression without semicolon.
rep(talent,'            };\n        }\n\n\t\treturn dmg;', '            }\n        }\n\n\t\treturn dmg;')

method='''    // Custom artwork indices for the Rune Knight; 0-16 are new abilities/talents.
    // 17-26 are new icons for the class's endgame armor ability talents.
    public int runeKnightIcon(){
        switch (this){
            case RUNIC_EDGE: return 0;
            case RUNIC_WARD: return 1;
            case RUNIC_SPARK: return 2;
            case RUNIC_BATTERY: return 3;
            case RUNIC_MASTERY: return 4;
            case RUNIC_RECOVERY: return 5;
            case RUNIC_ECHO: return 6;
            case RUNIC_OVERCHARGE: return 7;
            case RUNIC_HEART: return 8;
            case RUNIC_TITAN: return 9;
            case RUNIC_MOMENTUM: return 10;
            case RUNIC_FORTRESS: return 11;
            case RUNIC_AEGIS: return 12;
            case RUNIC_RESOLVE: return 13;
            case RUNIC_FURY: return 14;
            case RUNIC_EXECUTION: return 15;
            case RUNIC_FLOW: return 16;
            case BODY_SLAM: return 17;
            case IMPACT_WAVE: return 18;
            case DOUBLE_JUMP: return 19;
            case EXPANDING_WAVE: return 20;
            case STRIKING_WAVE: return 21;
            case SHOCK_FORCE: return 22;
            case SUSTAINED_RETRIBUTION: return 23;
            case SHRUG_IT_OFF: return 24;
            case EVEN_THE_ODDS: return 25;
            case HEROIC_ENERGY: return 26;
            default: return -1;
        }
    }

'''
rep(talent,'\tpublic int maxPoints(){', method+'\tpublic int maxPoints(){')

# No vanilla icons are used by new Rune Knight talents or subclass/ability buttons.
ui=code/'ui/TalentIcon.java'
rep(ui, 'import com.shatteredpixel.shatteredpixeldungeon.Assets;', '''import com.shatteredpixel.shatteredpixeldungeon.Assets;
import com.shatteredpixel.shatteredpixeldungeon.Dungeon;
import com.shatteredpixel.shatteredpixeldungeon.actors.hero.HeroClass;''')
rep(ui, '''	public TalentIcon(Talent talent){
		this(talent.icon());
	}

	public TalentIcon(int icon){
		super( Assets.Interfaces.TALENT_ICONS );

		if (film == null) film = new TextureFilm(texture, SIZE, SIZE);

		frame(film.get(icon));
	}''','''    public TalentIcon(Talent talent){
        super(useRuneArt(talent) ? Assets.Interfaces.RUNEKNIGHT_TALENTS : Assets.Interfaces.TALENT_ICONS);
        if (useRuneArt(talent)) {
            frame(new TextureFilm(texture, SIZE, SIZE).get(talent.runeKnightIcon()));
        } else {
            if (film == null) film = new TextureFilm(texture, SIZE, SIZE);
            frame(film.get(talent.icon()));
        }
    }

    private static boolean useRuneArt(Talent talent) {
        int index = talent.runeKnightIcon();
        return index >= 0 && (index <= 16 || (Dungeon.hero != null
                && Dungeon.hero.heroClass == HeroClass.RUNEKNIGHT));
    }

    public TalentIcon(int icon){
        super(Assets.Interfaces.TALENT_ICONS);
        if (film == null) film = new TextureFilm(texture, SIZE, SIZE);
        frame(film.get(icon));
    }''')

hi=code/'ui/HeroIcon.java'
rep(hi,'import com.shatteredpixel.shatteredpixeldungeon.Assets;', '''import com.shatteredpixel.shatteredpixeldungeon.Assets;
import com.shatteredpixel.shatteredpixeldungeon.Dungeon;
import com.shatteredpixel.shatteredpixeldungeon.actors.hero.HeroClass;''')
rep(hi,'public static final int PALADIN     = 11;', '''public static final int PALADIN     = 11;
    public static final int RUNE_SENTINEL = 12;
    public static final int RUNE_REAVER   = 13;''')
rep(hi, '''	public HeroIcon(HeroSubClass subCls){
		super( Assets.Interfaces.HERO_ICONS );
		if (film == null){
			film = new TextureFilm(texture, SIZE, SIZE);
		}
		frame(film.get(subCls.icon()));
	}''','''    public HeroIcon(HeroSubClass subCls){
        super((subCls == HeroSubClass.RUNE_SENTINEL || subCls == HeroSubClass.RUNE_REAVER)
                ? Assets.Interfaces.RUNEKNIGHT_SUBCLASSES : Assets.Interfaces.HERO_ICONS);
        if (subCls == HeroSubClass.RUNE_SENTINEL || subCls == HeroSubClass.RUNE_REAVER) {
            frame(new TextureFilm(texture, SIZE, SIZE).get(subCls.icon() - RUNE_SENTINEL));
        } else {
            if (film == null) film = new TextureFilm(texture, SIZE, SIZE);
            frame(film.get(subCls.icon()));
        }
    }''')
rep(hi, '''	public HeroIcon(ArmorAbility abil){
		super( Assets.Interfaces.HERO_ICONS );
		if (film == null){
			film = new TextureFilm(texture, SIZE, SIZE);
		}
		frame(film.get(abil.icon()));
	}''','''    private static boolean isRuneArmorArt(ArmorAbility abil){
        if (Dungeon.hero == null || Dungeon.hero.heroClass != HeroClass.RUNEKNIGHT) return false;
        String name = abil.getClass().getSimpleName();
        return name.equals("HeroicLeap") || name.equals("Shockwave") || name.equals("Endure");
    }

    public HeroIcon(ArmorAbility abil){
        super(isRuneArmorArt(abil) ? Assets.Interfaces.RUNEKNIGHT_ABILITIES : Assets.Interfaces.HERO_ICONS);
        if (isRuneArmorArt(abil)) {
            String name = abil.getClass().getSimpleName();
            int index = name.equals("HeroicLeap") ? 0 : name.equals("Shockwave") ? 1 : 2;
            frame(new TextureFilm(texture, SIZE, SIZE).get(index));
        } else {
            if (film == null) film = new TextureFilm(texture, SIZE, SIZE);
            frame(film.get(abil.icon()));
        }
    }''')

# Entire subclass and novel talent name/description bundles: English fallback and Korean.
ko=r'''
actors.hero.herosubclass.rune_sentinel=룬 수호자
actors.hero.herosubclass.rune_sentinel_short_desc=_룬 수호자_는 룬 폭발을 방어적으로 다루며 더 강한 보호막을 쌓습니다.
actors.hero.herosubclass.rune_sentinel_desc=룬 수호자는 룬을 각인한 방벽으로 적의 공격을 받아냅니다. 전직 특성으로 보호막, 유지 시간 및 재사용 대기시간을 강화할 수 있습니다.
actors.hero.herosubclass.rune_reaver=룬 약탈자
actors.hero.herosubclass.rune_reaver_short_desc=_룬 약탈자_는 룬 폭발을 공격적으로 다루며 큰 근접 피해를 줍니다.
actors.hero.herosubclass.rune_reaver_desc=룬 약탈자는 룬의 힘을 공격에 집중해 적에게 큰 피해를 입힙니다. 전직 특성으로 추가 피해, 처형 피해 및 지속시간을 강화합니다.
'''
en=r'''
actors.hero.herosubclass.rune_sentinel=Rune Sentinel
actors.hero.herosubclass.rune_sentinel_short_desc=The _Rune Sentinel_ specializes in protective runes and reinforced shielding.
actors.hero.herosubclass.rune_sentinel_desc=The Rune Sentinel uses engraved wards to withstand attacks. Subclass talents improve shielding, duration, and recovery.
actors.hero.herosubclass.rune_reaver=Rune Reaver
actors.hero.herosubclass.rune_reaver_short_desc=The _Rune Reaver_ specializes in offensive runes and heavy melee damage.
actors.hero.herosubclass.rune_reaver_desc=The Rune Reaver channels runic power into attacks. Subclass talents improve damage, execution damage, and duration.
'''
entries={
'r unic_dummy':('',''),
'runic_spark':('룬의 불꽃','룬 폭발 중 근접 피해가 특성 레벨마다 1 증가합니다.'),
'runic_battery':('룬 축전지','룬 폭발의 재사용 대기시간이 특성 레벨마다 1턴 감소합니다.'),
'runic_echo':('룬 메아리','룬 폭발 중 근접 피해가 특성 레벨마다 1 증가합니다.'),
'runic_overcharge':('과충전 룬','룬 폭발을 사용하면 특성 레벨마다 보호막 2를 얻습니다.'),
'runic_heart':('룬의 심장','룬 폭발 지속시간이 특성 레벨마다 1턴 증가합니다.'),
'runic_titan':('거인의 룬','룬 폭발을 사용하면 특성 레벨마다 보호막 1을 얻습니다.'),
'runic_momentum':('룬 가속','룬 폭발 중 근접 피해가 특성 레벨마다 1 증가합니다.'),
'runic_fortress':('룬 요새','룬 폭발을 사용하면 특성 레벨마다 보호막 3을 얻습니다.'),
'runic_aegis':('룬 방패','룬 폭발을 사용하면 특성 레벨마다 보호막 2를 얻습니다.'),
'runic_resolve':('룬 의지','룬 폭발 지속시간을 1턴 연장하고 재사용 대기시간을 1턴 줄입니다. 특성 레벨마다 적용됩니다.'),
'runic_fury':('룬 광전','룬 폭발 중 근접 피해가 특성 레벨마다 1 증가합니다.'),
'runic_execution':('룬 처형','체력이 절반 이하인 적을 룬 폭발 상태에서 공격할 때 특성 레벨마다 추가 피해 1을 줍니다.'),
'runic_flow':('룬 흐름','룬 폭발 지속시간이 특성 레벨마다 1턴 증가합니다.'),
}
en_entries={
'runic_spark':('Runic Spark','Runic Surge deals +1 melee damage per talent level.'),
'runic_battery':('Runic Battery','Runic Surge cooldown is reduced by 1 turn per talent level.'),
'runic_echo':('Runic Echo','Runic Surge deals +1 melee damage per talent level.'),
'runic_overcharge':('Runic Overcharge','Activating Runic Surge grants +2 shielding per talent level.'),
'runic_heart':('Runic Heart','Runic Surge lasts +1 turn per talent level.'),
'runic_titan':('Titan Rune','Activating Runic Surge grants +1 shielding per talent level.'),
'runic_momentum':('Rune Momentum','Runic Surge deals +1 melee damage per talent level.'),
'runic_fortress':('Rune Fortress','Activating Runic Surge grants +3 shielding per talent level.'),
'runic_aegis':('Rune Aegis','Activating Runic Surge grants +2 shielding per talent level.'),
'runic_resolve':('Rune Resolve','Runic Surge lasts 1 more turn and has 1 less turn of cooldown per talent level.'),
'runic_fury':('Rune Fury','Runic Surge deals +1 melee damage per talent level.'),
'runic_execution':('Rune Execution','Runic Surge attacks deal +1 damage per talent level to enemies below half health.'),
'runic_flow':('Rune Flow','Runic Surge lasts +1 turn per talent level.'),
}
for key,(name,desc) in entries.items():
    if key.startswith('r '): continue
    ko+=f'actors.hero.talent.{key}.title={name}\nactors.hero.talent.{key}.desc={desc}\n'
for key,(name,desc) in en_entries.items():
    en+=f'actors.hero.talent.{key}.title={name}\nactors.hero.talent.{key}.desc={desc}\n'
# Update localized class description to remove obsolete inherited-subclasses statement.
for lang, additions, old, new in [
    ('ko',ko,'이 초기 버전은 전사의 전직 및 영웅의 갑옷 능력을 공유합니다.','룬 수호자와 룬 약탈자 전직을 선택할 수 있습니다. 전용 전직 및 특성을 사용합니다.'),
    ('',en,'This initial mod reuses Warrior subclasses and armor abilities.','Choose Rune Sentinel or Rune Reaver, each with unique subclass talents.')
]:
    f=Path(f'core/src/main/assets/messages/actors/actors{("_"+lang) if lang else ""}.properties')
    rep(f,old,new)
    append(f,additions)

# Copy original 2D resources. Replace only the two declared, previously unused item atlas tiles.
for src,dest in [('sprites/runeknight.png','sprites/runeknight.png'),
                 ('splashes/runeknight.jpg','splashes/runeknight.jpg'),
                 ('interfaces/runeknight_talents.png','interfaces/runeknight_talents.png'),
                 ('interfaces/runeknight_subclasses.png','interfaces/runeknight_subclasses.png'),
                 ('interfaces/runeknight_abilities.png','interfaces/runeknight_abilities.png')]:
    target=root/'core/src/main/assets'/dest
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(assets/src,target)
    print('ASSET',dest)

orig=root/'core/src/main/assets/sprites/items.png'
item=Image.open(orig).convert('RGBA')
assert item.size==(256,512),f'Unexpected upstream item atlas size {item.size}'
for ix,fn in [(20,'runic_focus.png'),(25,'runeknight_armor.png')]:
    x=(ix%16)*16;y=(ix//16)*16
    item.paste((0,0,0,0),(x,y,x+16,y+16))
    item.alpha_composite(Image.open(assets/'sprites'/fn).convert('RGBA'),(x,y))
item.save(orig)
print('ASSET sprites/items.png: new original item slots 20 and 25')
print('Original Rune Knight visual resources and independent subclass talents installed.')