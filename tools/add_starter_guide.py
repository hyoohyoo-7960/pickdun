#!/usr/bin/env python3
"""Add a harmless, stationary AI guide next to the initial stairs on floor 1.
Run after tools/apply_to_shattered.py and before compiling the game.
"""
from pathlib import Path
import sys
repo = Path(sys.argv[1]).resolve()
root = repo / "core/src/main/java/com/shatteredpixel/shatteredpixeldungeon"
sewer = root / "levels/SewerLevel.java"
npc = root / "actors/mobs/npcs/AiGuide.java"
if not sewer.is_file() or not (root / "ai/AiNpcChat.java").is_file():
    raise SystemExit("Missing game checkout or AI NPC v0.1 patch")

npc.write_text("""/*
 * Shattered Pixel Dungeon AI NPC extension, GPL-3.0-or-later.
 * Dialogue-only starter guide, separate from the shopkeeper.
 */
package com.shatteredpixel.shatteredpixeldungeon.actors.mobs.npcs;

import com.shatteredpixel.shatteredpixeldungeon.Dungeon;
import com.shatteredpixel.shatteredpixeldungeon.actors.Char;
import com.shatteredpixel.shatteredpixeldungeon.actors.buffs.Buff;
import com.shatteredpixel.shatteredpixeldungeon.ai.AiNpcChat;
import com.shatteredpixel.shatteredpixeldungeon.sprites.WandmakerSprite;
import com.watabou.noosa.Game;
import com.watabou.utils.Callback;

public class AiGuide extends NPC {

    {
        spriteClass = WandmakerSprite.class;
        properties.add(Property.IMMOVABLE);
    }

    @Override
    public String name() {
        return "AI 안내자";
    }

    @Override
    public String description() {
        return "던전 입구에서 만나는 AI 안내자입니다. "
                + "대화를 선택해 ChatGPT 계정을 연결할 수 있습니다.";
    }

    @Override
    protected Char chooseEnemy() {
        return null;
    }

    @Override
    public int defenseSkill(Char enemy) {
        return INFINITE_EVASION;
    }

    @Override
    public void damage(int dmg, Object src) {
        // Conversation only, no combat.
    }

    @Override
    public boolean add(Buff buff) {
        return false;
    }

    @Override
    public boolean reset() {
        return true;
    }

    @Override
    public boolean interact(Char c) {
        if (c != Dungeon.hero) return true;
        if (sprite != null) sprite.turnTo(pos, c.pos);
        Game.runOnRenderThread(new Callback() {
            @Override public void call() {
                AiNpcChat.open(AiGuide.this);
            }
        });
        return true;
    }
}
""", encoding="utf-8")

s = sewer.read_text(encoding="utf-8")
if "spawnStartingAiGuide()" not in s:
    imp = "import com.shatteredpixel.shatteredpixeldungeon.actors.mobs.npcs.Ghost;"
    assert s.count(imp) == 1, "Cannot locate SewerLevel import"
    s = s.replace(imp, imp + "\nimport com.shatteredpixel.shatteredpixeldungeon.actors.mobs.npcs.AiGuide;\nimport com.watabou.utils.PathFinder;", 1)
    original = """\t@Override
\tprotected void createMobs() {
\t\tGhost.Quest.spawn( this, roomExit );
\t\tsuper.createMobs();
\t}"""
    changed = """\t@Override
\tprotected void createMobs() {
\t\tGhost.Quest.spawn( this, roomExit );
\t\tsuper.createMobs();
\t\tif (Dungeon.depth == 1 && Dungeon.branch == 0 && !Statistics.amuletObtained) {
\t\t\tspawnStartingAiGuide();
\t\t}
\t}

\t/** Position the guide on a safe tile immediately beside the player's entrance. */
\tprivate void spawnStartingAiGuide() {
\t\tint entranceCell = entrance();
\t\tint chosen = -1;
\t\tfor (int i : PathFinder.NEIGHBOURS4) {
\t\t\tint candidate = entranceCell + i;
\t\t\tif (freeGuideCell(candidate)) {
\t\t\t\tchosen = candidate;
\t\t\t\tbreak;
\t\t\t}
\t\t}
\t\tif (chosen == -1) {
\t\t\tfor (int i : PathFinder.NEIGHBOURS8) {
\t\t\t\tint candidate = entranceCell + i;
\t\t\t\tif (freeGuideCell(candidate)) {
\t\t\t\t\tchosen = candidate;
\t\t\t\t\tbreak;
\t\t\t\t}
\t\t\t}
\t\t}
\t\tif (chosen == -1) return; // Never prevent level generation.
\t\tAiGuide guide = new AiGuide();
\t\tguide.pos = chosen;
\t\tmobs.add(guide);
\t}

\tprivate boolean freeGuideCell(int cell) {
\t\treturn cell > 0 && cell < length()
\t\t\t\t&& cell != entrance() && cell != exit()
\t\t\t\t&& passable[cell] && !solid[cell]
\t\t\t\t&& findMob(cell) == null && traps.get(cell) == null;
\t}"""
    assert s.count(original) == 1, "Upstream SewerLevel.createMobs has changed"
    sewer.write_text(s.replace(original, changed, 1), encoding="utf-8")
print("AI guide now spawns beside the hero on floor 1.")
