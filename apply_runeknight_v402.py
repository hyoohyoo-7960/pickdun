#!/usr/bin/env python3
"""Add the Rune Knight demo class to the official Shattered Pixel Dungeon v4.0.2 source tree.

Run from any directory with: python3 apply_runeknight_v402.py /path/to/shattered-pixel-dungeon
License: GPL-3.0-or-later (matching upstream).
"""
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
CODE = Path('core/src/main/java/com/shatteredpixel/shatteredpixeldungeon')

def replace(file, old, new, count=1):
    path = ROOT / file
    content = path.read_text('utf-8')
    found = content.count(old)
    if found != count:
        raise RuntimeError(f'{file}: expected {count} occurrences; found {found}: {old[:110]!r}')
    path.write_text(content.replace(old,new,count), encoding='utf-8')
    print('Patched', file)

def append(file, content):
    path=ROOT/file
    with path.open('a', encoding='utf-8') as f:
        f.write('\n' + content.strip() + '\n')
    print('Localized', file)

hero = CODE / 'actors/hero/HeroClass.java'
replace(hero,
        'CLERIC( HeroSubClass.PRIEST, HeroSubClass.PALADIN );',
        'CLERIC( HeroSubClass.PRIEST, HeroSubClass.PALADIN ),\n\tRUNEKNIGHT( HeroSubClass.BERSERKER, HeroSubClass.GLADIATOR );')
replace(hero,
        'import com.shatteredpixel.shatteredpixeldungeon.items.Item;',
        'import com.shatteredpixel.shatteredpixeldungeon.items.Item;\nimport com.shatteredpixel.shatteredpixeldungeon.items.RunicFocus;')
replace(hero,
        '\t\t\tcase CLERIC:\n\t\t\t\tinitCleric( hero );\n\t\t\t\tbreak;',
        '\t\t\tcase CLERIC:\n\t\t\t\tinitCleric( hero );\n\t\t\t\tbreak;\n\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\tinitRuneKnight( hero );\n\t\t\t\tbreak;')
replace(hero,
        '\tprivate static void initMage( Hero hero ) {',
        '''\tprivate static void initRuneKnight( Hero hero ) {
        // Retain the standard Warrior equipment and seal, but grant a unique active skill.
        initWarrior(hero);
        RunicFocus focus = new RunicFocus();
        focus.identify().collect();
        Dungeon.quickslot.setSlot(1, focus);
    }

\tprivate static void initMage( Hero hero ) {''')
replace(hero,
        '\t\t\tcase CLERIC:\n\t\t\t\treturn Badges.Badge.MASTERY_CLERIC;',
        '\t\t\tcase CLERIC:\n\t\t\t\treturn Badges.Badge.MASTERY_CLERIC;\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\treturn Badges.Badge.MASTERY_WARRIOR;')
replace(hero,
        '\t\t\tcase CLERIC:\n\t\t\t\treturn Badges.isUnlocked(Badges.Badge.UNLOCK_CLERIC);',
        '\t\t\tcase CLERIC:\n\t\t\t\treturn Badges.isUnlocked(Badges.Badge.UNLOCK_CLERIC);\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\treturn true;')

armor = CODE / 'items/armor/ClassArmor.java'
replace(armor,
        '\t\t\tcase WARRIOR:\n\t\t\t\tclassArmor = new WarriorArmor();',
        '\t\t\tcase WARRIOR:\n\t\t\tcase RUNEKNIGHT:\n\t\t\t\tclassArmor = new WarriorArmor();')

talent=CODE/'actors/hero/Talent.java'
replace(talent,
        'import com.shatteredpixel.shatteredpixeldungeon.items.Item;',
        'import com.shatteredpixel.shatteredpixeldungeon.items.Item;\nimport com.shatteredpixel.shatteredpixeldungeon.items.RunicFocus;')
replace(talent,
        '\t//universal T4',
        '''\t// Rune Knight: existing icon indices intentionally reused until custom art is available.
    RUNIC_EDGE(34), RUNIC_WARD(35), RUNIC_MASTERY(37), RUNIC_RECOVERY(39),

\t//universal T4''')
replace(talent,
        '\t\t\tcase CLERIC:\n\t\t\t\tCollections.addAll(tierTalents, SATIATED_SPELLS, HOLY_INTUITION, SEARING_LIGHT, SHIELD_OF_LIGHT);',
        '\t\t\tcase RUNEKNIGHT:\n\t\t\t\tCollections.addAll(tierTalents, RUNIC_EDGE, RUNIC_WARD, PATIENT_STRIKE, AGGRESSIVE_BARRIER);\n\t\t\t\tbreak;\n\t\t\tcase CLERIC:\n\t\t\t\tCollections.addAll(tierTalents, SATIATED_SPELLS, HOLY_INTUITION, SEARING_LIGHT, SHIELD_OF_LIGHT);')
replace(talent,
        '\t\t\tcase CLERIC:\n\t\t\t\tCollections.addAll(tierTalents, ENLIGHTENING_MEAL, RECALL_INSCRIPTION, SUNRAY, DIVINE_SENSE, BLESS);',
        '\t\t\tcase RUNEKNIGHT:\n\t\t\t\tCollections.addAll(tierTalents, RUNIC_MASTERY, RUNIC_RECOVERY, WEAPON_RECHARGING, LETHAL_HASTE, SWIFT_EQUIP);\n\t\t\t\tbreak;\n\t\t\tcase CLERIC:\n\t\t\t\tCollections.addAll(tierTalents, ENLIGHTENING_MEAL, RECALL_INSCRIPTION, SUNRAY, DIVINE_SENSE, BLESS);')
replace(talent,
        '\t\t\tcase CLERIC:\n\t\t\t\tCollections.addAll(tierTalents, CLEANSE, LIGHT_READING);',
        '\t\t\tcase RUNEKNIGHT:\n\t\t\t\tCollections.addAll(tierTalents, HOLD_FAST, STRONGMAN);\n\t\t\t\tbreak;\n\t\t\tcase CLERIC:\n\t\t\t\tCollections.addAll(tierTalents, CLEANSE, LIGHT_READING);')
replace(talent,
        '\n\t\treturn dmg;\n\t}\n\n\tpublic static class ProvokedAngerTracker',
        '''
        // Rune Surge only empowers melee strikes; Rune Edge scales with invested talent points.
        if (hero.buff(RunicFocus.RunicSurge.class) != null
                && !(hero.belongings.attackingWeapon() instanceof MissileWeapon)) {
            dmg += 2 + hero.pointsInTalent(RUNIC_EDGE);
        }

\t\treturn dmg;
\t}

\tpublic static class ProvokedAngerTracker''')

focus=ROOT/CODE/'items/RunicFocus.java'
if focus.exists():
    raise RuntimeError('Refusing to overwrite '+str(focus))
focus.write_text('''/*
 * Shattered Pixel Dungeon - Rune Knight demo module
 * Copyright (C) 2026 Rune Knight mod contributors
 * GPL-3.0-or-later; see upstream LICENSE.txt.
 */
package com.shatteredpixel.shatteredpixeldungeon.items;

import com.shatteredpixel.shatteredpixeldungeon.actors.buffs.Barrier;
import com.shatteredpixel.shatteredpixeldungeon.actors.buffs.Buff;
import com.shatteredpixel.shatteredpixeldungeon.actors.buffs.FlavourBuff;
import com.shatteredpixel.shatteredpixeldungeon.actors.hero.Hero;
import com.shatteredpixel.shatteredpixeldungeon.actors.hero.Talent;
import com.shatteredpixel.shatteredpixeldungeon.messages.Messages;
import com.shatteredpixel.shatteredpixeldungeon.sprites.ItemSpriteSheet;
import com.shatteredpixel.shatteredpixeldungeon.ui.BuffIndicator;
import com.shatteredpixel.shatteredpixeldungeon.utils.GLog;
import com.watabou.noosa.Image;

import java.util.ArrayList;

/** Reusable class-bound item whose cooldown is tracked by a savable buff. */
public class RunicFocus extends Item {

    private static final String AC_SURGE = "SURGE";

    {
        image = ItemSpriteSheet.WAND_MAGIC_MISSILE;
        unique = true;
        bones = false;
        defaultAction = AC_SURGE;
    }

    @Override
    public ArrayList<String> actions(Hero hero) {
        ArrayList<String> actions = super.actions(hero);
        actions.remove(AC_DROP);
        actions.remove(AC_THROW);
        actions.add(AC_SURGE);
        return actions;
    }

    @Override
    public void execute(Hero hero, String action) {
        super.execute(hero, action);
        if (!AC_SURGE.equals(action)) return;
        if (hero.buff(RunicCooldown.class) != null) {
            GLog.w(Messages.get(this, "cooldown"));
            return;
        }

        float duration = 5f + 2f * hero.pointsInTalent(Talent.RUNIC_MASTERY);
        Buff.prolong(hero, RunicSurge.class, duration);
        if (hero.hasTalent(Talent.RUNIC_WARD)) {
            Buff.affect(hero, Barrier.class).incShield(2 * hero.pointsInTalent(Talent.RUNIC_WARD));
        }
        float cooldown = Math.max(4f, 12f - 2f * hero.pointsInTalent(Talent.RUNIC_RECOVERY));
        Buff.prolong(hero, RunicCooldown.class, cooldown);
        GLog.p(Messages.get(this, "activated"));
        hero.sprite.operate(hero.pos);
        hero.spendAndNext(1f);
    }

    public static class RunicSurge extends FlavourBuff {
        {
            type = buffType.POSITIVE;
            announced = true;
        }
        @Override public int icon() { return BuffIndicator.WEAPON; }
        @Override public void tintIcon(Image icon) { icon.hardlight(0.6f, 0.9f, 1.2f); }
    }

    public static class RunicCooldown extends FlavourBuff {
        @Override public int icon() { return BuffIndicator.TIME; }
        @Override public void tintIcon(Image icon) { icon.hardlight(0.6f, 0.8f, 1f); }
    }
}
''',encoding='utf-8')
print('Created', focus)

append(Path('core/src/main/assets/messages/actors/actors_ko.properties'), r'''
# Rune Knight community mod
actors.hero.heroclass.runeknight=룬 기사
actors.hero.heroclass.runeknight_desc_short=룬 기사는 전용 도구 _룬 초점_으로 전투 중 근접 공격을 강화하며, 특성으로 보호막과 지속시간을 성장시킵니다.
actors.hero.heroclass.runeknight_desc=룬 기사는 전사의 기본 장비와 _룬 초점_을 가지고 시작합니다. 룬 초점을 사용하면 5턴 동안 근접 공격에 2의 추가 피해를 주며, 기본 재사용 대기시간은 12턴입니다. 특성으로 공격력, 보호막, 지속시간, 재사용 대기시간을 강화할 수 있습니다.\n\n이 초기 버전은 전사의 전직 및 영웅의 갑옷 능력을 공유합니다.
actors.hero.heroclass.runeknight_unlock=룬 기사는 기본적으로 해금되어 있습니다.
actors.hero.talent.runic_edge.title=룬의 칼날
actors.hero.talent.runic_edge.desc=_+1:_ 룬 폭발 중 근접 공격의 추가 피해 +1.\n\n_+2:_ 추가 피해 +2.
actors.hero.talent.runic_ward.title=룬의 방벽
actors.hero.talent.runic_ward.desc=_+1:_ 룬 폭발 사용 시 보호막 2 획득.\n\n_+2:_ 보호막 4 획득.
actors.hero.talent.runic_mastery.title=룬 숙련
actors.hero.talent.runic_mastery.desc=_+1:_ 룬 폭발 지속시간 2턴 증가.\n\n_+2:_ 지속시간 4턴 증가.
actors.hero.talent.runic_recovery.title=룬 순환
actors.hero.talent.runic_recovery.desc=_+1:_ 룬 폭발 재사용 대기시간 2턴 감소.\n\n_+2:_ 재사용 대기시간 4턴 감소.
''')
append(Path('core/src/main/assets/messages/actors/actors.properties'), r'''
# Rune Knight community mod
actors.hero.heroclass.runeknight=Rune Knight
actors.hero.heroclass.runeknight_desc_short=The Rune Knight uses a reusable _Runic Focus_ to empower melee strikes and can improve its shield, uptime and cooldown via talents.
actors.hero.heroclass.runeknight_desc=The Rune Knight begins with Warrior equipment plus a _Runic Focus_. Runic Surge boosts melee damage by 2 for 5 turns, with a 12-turn cooldown. Its talents boost damage, shielding, duration, and recovery.\n\nThis initial mod reuses Warrior subclasses and armor abilities.
actors.hero.heroclass.runeknight_unlock=Rune Knight is unlocked by default.
actors.hero.talent.runic_edge.title=Runic Edge
actors.hero.talent.runic_edge.desc=_+1:_ Increase Runic Surge's melee bonus damage by 1.\n\n_+2:_ Increase it by 2.
actors.hero.talent.runic_ward.title=Runic Ward
actors.hero.talent.runic_ward.desc=_+1:_ Gain 2 shielding when activating Runic Surge.\n\n_+2:_ Gain 4 shielding.
actors.hero.talent.runic_mastery.title=Runic Mastery
actors.hero.talent.runic_mastery.desc=_+1:_ Runic Surge lasts 2 more turns.\n\n_+2:_ It lasts 4 more turns.
actors.hero.talent.runic_recovery.title=Runic Recovery
actors.hero.talent.runic_recovery.desc=_+1:_ Runic Surge cooldown is 2 turns shorter.\n\n_+2:_ It is 4 turns shorter.
''')
append(Path('core/src/main/assets/messages/items/items_ko.properties'), r'''
# Rune Knight community mod
items.runicfocus.name=룬 초점
items.runicfocus.desc=룬 기사가 사용하는 고유 전투 도구입니다. 사용하면 5턴 동안 근접 공격에 2의 추가 피해를 주며 재사용 대기시간은 12턴입니다. 특성을 통해 향상됩니다.
items.runicfocus.ac_surge=룬 폭발
items.runicfocus.cooldown=룬 폭발이 아직 재사용 대기 중입니다.
items.runicfocus.activated=룬의 힘이 검에 깃듭니다!
items.runicfocus$runicsurge.name=룬 폭발
items.runicfocus$runicsurge.desc=근접 공격의 추가 피해가 증가합니다. 남은 턴: %s.
items.runicfocus$runiccooldown.name=룬 초점 재충전
items.runicfocus$runiccooldown.desc=룬 폭발의 재사용 대기시간입니다. 남은 턴: %s.
''')
append(Path('core/src/main/assets/messages/items/items.properties'), r'''
# Rune Knight community mod
items.runicfocus.name=Runic Focus
items.runicfocus.desc=The Rune Knight's unique reusable battle tool. Grants +2 melee damage for 5 turns on a 12-turn cooldown. Talents improve its effects.
items.runicfocus.ac_surge=RUNIC SURGE
items.runicfocus.cooldown=Runic Surge is still recharging.
items.runicfocus.activated=Runic energy surges through your weapon!
items.runicfocus$runicsurge.name=Runic Surge
items.runicfocus$runicsurge.desc=Melee attacks deal extra damage. Remaining turns: %s.
items.runicfocus$runiccooldown.name=Runic Recharge
items.runicfocus$runiccooldown.desc=Runic Surge is recharging. Remaining turns: %s.
''')

build = Path('build.gradle')
replace(build,"appName = 'Shattered Pixel Dungeon'","appName = 'Rune Knight Pixel Dungeon'")
replace(build,"appPackageName = 'com.shatteredpixel.shatteredpixeldungeon'", "appPackageName = 'com.shatteredpixel.shatteredpixeldungeon.runeknight'")
replace(build,"appVersionCode = 922", "appVersionCode = 923")
replace(build,"appVersionName = '4.0.2'", "appVersionName = '4.0.2-RK1'")
print('Rune Knight mod overlay applied for Shattered Pixel Dungeon v4.0.2')