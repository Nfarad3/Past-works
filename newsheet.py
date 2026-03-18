#!/usr/bin/env python3
"""D&D 5e Character Abilities Lister"""

# --- Data Tables ---

STATS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

PROFICIENCY_BONUS = {
    1: 2, 2: 2, 3: 2, 4: 2,
    5: 3, 6: 3, 7: 3, 8: 3,
    9: 4, 10: 4, 11: 4, 12: 4,
    13: 5, 14: 5, 15: 5, 16: 5,
    17: 6, 18: 6, 19: 6, 20: 6,
}

HIT_DICE = {
    "Barbarian": 12, "Bard": 8, "Cleric": 8, "Druid": 8,
    "Fighter": 10, "Monk": 8, "Paladin": 10, "Ranger": 10,
    "Rogue": 8, "Sorcerer": 6, "Warlock": 8, "Wizard": 6,
}

CLASS_PROFICIENCIES = {
    "Barbarian": {
        "armor": ["Light armor", "Medium armor", "Shields"],
        "weapons": ["Simple weapons", "Martial weapons"],
        "tools": [],
        "saving_throws": ["Strength", "Constitution"],
        "skills": "Choose 2: Animal Handling, Athletics, Intimidation, Nature, Perception, Survival",
    },
    "Bard": {
        "armor": ["Light armor"],
        "weapons": ["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
        "tools": ["Three musical instruments of your choice"],
        "saving_throws": ["Dexterity", "Charisma"],
        "skills": "Choose any 3 skills",
    },
    "Cleric": {
        "armor": ["Light armor", "Medium armor", "Shields"],
        "weapons": ["Simple weapons"],
        "tools": [],
        "saving_throws": ["Wisdom", "Charisma"],
        "skills": "Choose 2: History, Insight, Medicine, Persuasion, Religion",
    },
    "Druid": {
        "armor": ["Light armor", "Medium armor", "Shields (non-metal)"],
        "weapons": ["Clubs", "Daggers", "Darts", "Javelins", "Maces", "Quarterstaffs", "Scimitars", "Sickles", "Slings", "Spears"],
        "tools": ["Herbalism kit"],
        "saving_throws": ["Intelligence", "Wisdom"],
        "skills": "Choose 2: Arcana, Animal Handling, Insight, Medicine, Nature, Perception, Religion, Survival",
    },
    "Fighter": {
        "armor": ["All armor", "Shields"],
        "weapons": ["Simple weapons", "Martial weapons"],
        "tools": [],
        "saving_throws": ["Strength", "Constitution"],
        "skills": "Choose 2: Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, Survival",
    },
    "Monk": {
        "armor": [],
        "weapons": ["Simple weapons", "Shortswords"],
        "tools": ["One artisan's tool type or one musical instrument"],
        "saving_throws": ["Strength", "Dexterity"],
        "skills": "Choose 2: Acrobatics, Athletics, History, Insight, Religion, Stealth",
    },
    "Paladin": {
        "armor": ["All armor", "Shields"],
        "weapons": ["Simple weapons", "Martial weapons"],
        "tools": [],
        "saving_throws": ["Wisdom", "Charisma"],
        "skills": "Choose 2: Athletics, Insight, Intimidation, Medicine, Persuasion, Religion",
    },
    "Ranger": {
        "armor": ["Light armor", "Medium armor", "Shields"],
        "weapons": ["Simple weapons", "Martial weapons"],
        "tools": [],
        "saving_throws": ["Strength", "Dexterity"],
        "skills": "Choose 3: Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, Survival",
    },
    "Rogue": {
        "armor": ["Light armor"],
        "weapons": ["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
        "tools": ["Thieves' tools"],
        "saving_throws": ["Dexterity", "Intelligence"],
        "skills": "Choose 4: Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion, Sleight of Hand, Stealth",
    },
    "Sorcerer": {
        "armor": [],
        "weapons": ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        "tools": [],
        "saving_throws": ["Constitution", "Charisma"],
        "skills": "Choose 2: Arcana, Deception, Insight, Intimidation, Persuasion, Religion",
    },
    "Warlock": {
        "armor": ["Light armor"],
        "weapons": ["Simple weapons"],
        "tools": [],
        "saving_throws": ["Wisdom", "Charisma"],
        "skills": "Choose 2: Arcana, Deception, History, Intimidation, Investigation, Nature, Religion",
    },
    "Wizard": {
        "armor": [],
        "weapons": ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        "tools": [],
        "saving_throws": ["Intelligence", "Wisdom"],
        "skills": "Choose 2: Arcana, History, Insight, Investigation, Medicine, Religion",
    },
}

CLASS_FEATURES = {
    "Barbarian": {
        1:  ["Rage (2/rest, +2 damage; advantage on STR checks/saves, resistance to B/P/S damage)",
             "Unarmored Defense (AC = 10 + DEX mod + CON mod, no armor)"],
        2:  ["Reckless Attack (advantage on STR attacks this turn; enemies have advantage against you)",
             "Danger Sense (advantage on DEX saves vs. visible sources)"],
        3:  ["Primal Path (choose subclass)", "Rage uses increase to 3/rest"],
        4:  ["Ability Score Improvement"],
        5:  ["Extra Attack (attack twice per Attack action)",
             "Fast Movement (+10 ft. speed without heavy armor)"],
        6:  ["Primal Path feature", "Rage uses increase to 4/rest"],
        7:  ["Feral Instinct (advantage on Initiative; can act on first turn even if surprised while raging)"],
        8:  ["Ability Score Improvement"],
        9:  ["Brutal Critical (roll 1 extra damage die on a melee crit)", "Rage damage bonus increases to +3"],
        10: ["Primal Path feature"],
        11: ["Relentless Rage (DC 10 CON save to stay at 1 HP when dropped to 0 while raging; DC increases by 5 each use)"],
        12: ["Ability Score Improvement", "Rage uses increase to 5/rest"],
        13: ["Brutal Critical (2 extra damage dice on melee crit)"],
        14: ["Primal Path feature"],
        15: ["Persistent Rage (rage ends only if unconscious or you choose to end it)"],
        16: ["Ability Score Improvement", "Rage damage bonus increases to +4"],
        17: ["Brutal Critical (3 extra damage dice on melee crit)", "Rage uses increase to 6/rest"],
        18: ["Indomitable Might (STR ability check result minimum equals your STR score)"],
        19: ["Ability Score Improvement"],
        20: ["Primal Champion (+4 STR, +4 CON)", "Unlimited Rage uses"],
    },
    "Bard": {
        1:  ["Spellcasting (CHA-based, see spell list)",
             "Bardic Inspiration (grant d6 to ally's roll; CHA mod uses/rest)"],
        2:  ["Jack of All Trades (add half prof. bonus to non-proficient ability checks)",
             "Song of Rest (allies regain extra d6 HP on short rest)"],
        3:  ["Bard College (choose subclass)",
             "Expertise (double proficiency bonus for 2 chosen skills)"],
        4:  ["Ability Score Improvement"],
        5:  ["Bardic Inspiration die increases to d8",
             "Font of Inspiration (regain Bardic Inspiration on short rests)"],
        6:  ["Countercharm (action: allies within 30 ft. have advantage vs. charm/frighten)",
             "Bard College feature"],
        7:  ["Ability Score Improvement"],
        8:  ["Ability Score Improvement"],
        9:  ["Song of Rest die increases to d8"],
        10: ["Bardic Inspiration die increases to d10",
             "Expertise (2 more skills)",
             "Magical Secrets (learn 2 spells from any class list)"],
        11: ["Ability Score Improvement"],
        12: ["Ability Score Improvement"],
        13: ["Song of Rest die increases to d10"],
        14: ["Magical Secrets (2 more spells from any class)",
             "Bard College feature"],
        15: ["Bardic Inspiration die increases to d12"],
        16: ["Ability Score Improvement"],
        17: ["Song of Rest die increases to d12"],
        18: ["Magical Secrets (2 more spells from any class)"],
        19: ["Ability Score Improvement"],
        20: ["Superior Inspiration (regain 1 Bardic Inspiration on initiative if you have none)"],
    },
    "Cleric": {
        1:  ["Spellcasting (WIS-based)", "Divine Domain (choose subclass)", "Domain Spells (always prepared)"],
        2:  ["Channel Divinity (1/rest — Turn Undead + domain option)", "Divine Domain feature"],
        3:  ["Domain Spells (3rd-level)"],
        4:  ["Ability Score Improvement"],
        5:  ["Destroy Undead (CR 1/2 or lower undead are destroyed by Turn Undead)",
             "Domain Spells (5th-level)"],
        6:  ["Channel Divinity (2 uses/rest)", "Divine Domain feature"],
        7:  ["Domain Spells (7th-level)"],
        8:  ["Ability Score Improvement",
             "Destroy Undead (CR 1 or lower)",
             "Divine Domain feature"],
        9:  ["Domain Spells (9th-level)"],
        10: ["Divine Intervention (call on deity; % chance = cleric level)"],
        11: ["Destroy Undead (CR 2 or lower)"],
        12: ["Ability Score Improvement"],
        14: ["Destroy Undead (CR 3 or lower)"],
        17: ["Destroy Undead (CR 4 or lower)", "Divine Domain feature"],
        18: ["Channel Divinity (3 uses/rest)"],
        19: ["Ability Score Improvement"],
        20: ["Divine Intervention (guaranteed success)"],
    },
    "Druid": {
        1:  ["Druidic (secret language known only to druids)",
             "Spellcasting (WIS-based, ritual casting)"],
        2:  ["Wild Shape (CR 1/4 max, no fly/swim speed, 2 uses/rest)",
             "Druid Circle (choose subclass)"],
        4:  ["Wild Shape (CR 1/2 max, no fly speed)",
             "Ability Score Improvement"],
        6:  ["Druid Circle feature"],
        8:  ["Wild Shape (CR 1 max)", "Ability Score Improvement"],
        10: ["Druid Circle feature"],
        12: ["Ability Score Improvement"],
        14: ["Druid Circle feature"],
        16: ["Ability Score Improvement"],
        18: ["Timeless Body (age 10x slower; immune to magical aging)",
             "Beast Spells (cast spells in Wild Shape form, no S/M components)"],
        19: ["Ability Score Improvement"],
        20: ["Archdruid (unlimited Wild Shape uses)"],
    },
    "Fighter": {
        1:  ["Fighting Style (choose one: Archery, Defense, Dueling, Great Weapon, Protection, Two-Weapon)",
             "Second Wind (bonus action: regain 1d10 + Fighter level HP, 1/rest)"],
        2:  ["Action Surge (take one extra action on your turn, 1/rest)"],
        3:  ["Martial Archetype (choose subclass)"],
        4:  ["Ability Score Improvement"],
        5:  ["Extra Attack (attack twice per Attack action)"],
        6:  ["Ability Score Improvement"],
        7:  ["Martial Archetype feature"],
        8:  ["Ability Score Improvement"],
        9:  ["Indomitable (reroll a failed saving throw, 1/rest)"],
        10: ["Martial Archetype feature"],
        11: ["Extra Attack (attack three times per Attack action)"],
        12: ["Ability Score Improvement"],
        13: ["Indomitable (2 uses/rest)"],
        14: ["Ability Score Improvement"],
        15: ["Martial Archetype feature"],
        16: ["Ability Score Improvement"],
        17: ["Action Surge (2 uses/rest)", "Indomitable (3 uses/rest)"],
        18: ["Martial Archetype feature"],
        19: ["Ability Score Improvement"],
        20: ["Extra Attack (attack four times per Attack action)"],
    },
    "Monk": {
        1:  ["Unarmored Defense (AC = 10 + DEX mod + WIS mod, no armor/shield)",
             "Martial Arts (use DEX for monk weapon attacks; d4 unarmed damage; bonus unarmed after attack)"],
        2:  ["Ki (ki points = monk level; recharge on short/long rest)",
             "  - Flurry of Blows (2 ki): Two bonus unarmed strikes after Attack action",
             "  - Patient Defense (1 ki): Take Dodge as bonus action",
             "  - Step of the Wind (1 ki): Take Dash or Disengage as bonus action; jump distance doubled",
             "Unarmored Movement (+10 ft. speed, no armor/shield)"],
        3:  ["Monastic Tradition (choose subclass)",
             "Deflect Missiles (reaction: reduce ranged damage by 1d10 + DEX + monk level; catch and throw if reduced to 0)"],
        4:  ["Ability Score Improvement",
             "Slow Fall (reaction: reduce fall damage by 5 × monk level)"],
        5:  ["Extra Attack (attack twice per Attack action)",
             "Stunning Strike (1 ki after hit: CON save or stunned until end of your next turn)"],
        6:  ["Ki-Empowered Strikes (unarmed attacks count as magical)",
             "Monastic Tradition feature",
             "Unarmored Movement (+15 ft.)"],
        7:  ["Evasion (no damage on successful DEX save vs. area effects; half on failure)",
             "Stillness of Mind (action: end charmed or frightened condition on yourself)"],
        8:  ["Ability Score Improvement"],
        9:  ["Unarmored Movement (+15 ft.; walk along walls and across water at end of turn)"],
        10: ["Purity of Body (immune to disease and poison)", "Unarmored Movement (+20 ft.)"],
        11: ["Monastic Tradition feature"],
        12: ["Ability Score Improvement"],
        13: ["Tongue of the Sun and Moon (understand all spoken languages; all understand you)"],
        14: ["Diamond Soul (proficiency in all saving throws; spend 1 ki to reroll failed save)",
             "Unarmored Movement (+25 ft.)"],
        15: ["Timeless Body (no aging effects; no food or water needed)"],
        16: ["Ability Score Improvement"],
        17: ["Quivering Palm (3 ki after hit: vibrations last indefinitely; action to deal 10d10 necrotic or drop to 0 HP, CON save halves)"],
        18: ["Empty Body (4 ki: invisible + resistance to all but force for 1 min; 8 ki: cast Astral Projection)",
             "Unarmored Movement (+30 ft.)"],
        19: ["Ability Score Improvement"],
        20: ["Perfect Self (regain 4 ki on initiative roll if you have 0)"],
    },
    "Paladin": {
        1:  ["Divine Sense (1 + CHA mod uses/day: detect celestials, fiends, undead within 60 ft.)",
             "Lay on Hands (pool of 5 × paladin level HP/day; cure disease/poison for 5 HP)"],
        2:  ["Fighting Style",
             "Spellcasting (CHA-based)",
             "Divine Smite (expend spell slot after hit: 2d8 + 1d8/slot level radiant; +1d8 vs. undead/fiends)"],
        3:  ["Divine Health (immune to disease)",
             "Sacred Oath (choose subclass)",
             "Channel Divinity (1/rest — oath-specific options)"],
        4:  ["Ability Score Improvement"],
        5:  ["Extra Attack (attack twice per Attack action)"],
        6:  ["Aura of Protection (you and allies within 10 ft. add CHA mod to saving throws)"],
        7:  ["Sacred Oath feature"],
        8:  ["Ability Score Improvement"],
        10: ["Aura of Courage (you and allies within 10 ft. can't be frightened while you're conscious)"],
        11: ["Improved Divine Smite (melee weapon attacks deal extra 1d8 radiant damage)"],
        12: ["Ability Score Improvement"],
        14: ["Cleansing Touch (CHA mod uses/day: action to end one spell effect on willing creature by touch)"],
        15: ["Sacred Oath feature"],
        16: ["Ability Score Improvement"],
        18: ["Aura of Protection and Aura of Courage expand to 30 ft. range"],
        19: ["Ability Score Improvement"],
        20: ["Sacred Oath capstone feature"],
    },
    "Ranger": {
        1:  ["Favored Enemy (2 creature types: advantage on Survival to track, advantage on INT checks about them)",
             "Natural Explorer (1 favored terrain: double proficiency on INT/WIS checks; benefits while traveling)"],
        2:  ["Fighting Style", "Spellcasting (WIS-based)"],
        3:  ["Ranger Archetype (choose subclass)",
             "Primeval Awareness (expend spell slot: sense creature types within 1 mile/6 miles in favored terrain)"],
        4:  ["Ability Score Improvement"],
        5:  ["Extra Attack (attack twice per Attack action)"],
        6:  ["Favored Enemy (additional type)", "Natural Explorer (additional terrain)"],
        7:  ["Ranger Archetype feature"],
        8:  ["Ability Score Improvement",
             "Land's Stride (move through non-magical difficult terrain at normal speed; advantage vs. magical plants)"],
        9:  [],
        10: ["Natural Explorer (additional terrain)",
             "Hide in Plain Sight (spend 1 min to camouflage; +10 to Stealth while motionless)"],
        11: ["Ranger Archetype feature"],
        12: ["Ability Score Improvement"],
        14: ["Favored Enemy (additional type)",
             "Vanish (Hide as bonus action; can't be tracked by non-magical means)"],
        15: ["Ranger Archetype feature"],
        16: ["Ability Score Improvement"],
        18: ["Feral Senses (no disadvantage attacking invisible; sense invisible within 30 ft.)"],
        19: ["Ability Score Improvement"],
        20: ["Foe Slayer (once per turn, add WIS mod to attack or damage roll vs. Favored Enemy)"],
    },
    "Rogue": {
        1:  ["Expertise (double proficiency for 2 skills + thieves' tools)",
             "Sneak Attack (1d6 — extra damage once/turn when you have advantage or an ally is adjacent)",
             "Thieves' Cant (secret rogue language and signals)"],
        2:  ["Cunning Action (bonus action: Dash, Disengage, or Hide)", "Sneak Attack: 1d6"],
        3:  ["Roguish Archetype (choose subclass)", "Sneak Attack: 2d6"],
        4:  ["Ability Score Improvement", "Sneak Attack: 2d6"],
        5:  ["Uncanny Dodge (reaction: halve damage from attacker you can see)", "Sneak Attack: 3d6"],
        6:  ["Expertise (2 more skills)", "Sneak Attack: 3d6"],
        7:  ["Evasion (no damage on successful DEX save; half on failure)", "Sneak Attack: 4d6"],
        8:  ["Ability Score Improvement", "Sneak Attack: 4d6"],
        9:  ["Roguish Archetype feature", "Sneak Attack: 5d6"],
        10: ["Ability Score Improvement", "Sneak Attack: 5d6"],
        11: ["Reliable Talent (minimum roll of 10 on any proficient ability check)", "Sneak Attack: 6d6"],
        12: ["Ability Score Improvement", "Sneak Attack: 6d6"],
        13: ["Roguish Archetype feature", "Sneak Attack: 7d6"],
        14: ["Blindsense (aware of hidden/invisible within 10 ft. if you can hear)", "Sneak Attack: 7d6"],
        15: ["Slippery Mind (gain proficiency in WIS saving throws)", "Sneak Attack: 8d6"],
        16: ["Ability Score Improvement", "Sneak Attack: 8d6"],
        17: ["Roguish Archetype feature", "Sneak Attack: 9d6"],
        18: ["Elusive (attackers never have advantage on attack rolls against you)", "Sneak Attack: 9d6"],
        19: ["Ability Score Improvement", "Sneak Attack: 10d6"],
        20: ["Stroke of Luck (1/rest: missed attack becomes a hit OR failed check becomes a 20)", "Sneak Attack: 10d6"],
    },
    "Sorcerer": {
        1:  ["Spellcasting (CHA-based)", "Sorcerous Origin (choose subclass)"],
        2:  ["Font of Magic (sorcery points = sorcerer level)",
             "Flexible Casting (convert spell slots <-> sorcery points per table)"],
        3:  ["Metamagic (choose 2 options)",
             "  Options: Careful, Distant, Empowered, Extended, Heightened, Quickened, Subtle, Twinned"],
        4:  ["Ability Score Improvement"],
        6:  ["Sorcerous Origin feature"],
        8:  ["Ability Score Improvement"],
        10: ["Metamagic (1 additional option)"],
        12: ["Ability Score Improvement"],
        14: ["Sorcerous Origin feature"],
        16: ["Ability Score Improvement"],
        17: ["Metamagic (1 additional option)"],
        18: ["Sorcerous Origin feature"],
        19: ["Ability Score Improvement"],
        20: ["Sorcerous Restoration (regain 4 sorcery points on short rest)"],
    },
    "Warlock": {
        1:  ["Otherworldly Patron (choose subclass)",
             "Pact Magic (CHA-based; short rest recovery; slots per Warlock table)"],
        2:  ["Eldritch Invocations (choose 2 — passive/active enhancements to your powers)"],
        3:  ["Pact Boon (choose: Pact of the Chain, Blade, or Tome)"],
        4:  ["Ability Score Improvement"],
        5:  ["Eldritch Invocations (1 additional)"],
        6:  ["Otherworldly Patron feature"],
        7:  ["Eldritch Invocations (1 additional)"],
        8:  ["Ability Score Improvement"],
        9:  ["Eldritch Invocations (1 additional)"],
        10: ["Otherworldly Patron feature"],
        11: ["Mystic Arcanum (cast one 6th-level spell 1/day without a slot)"],
        12: ["Ability Score Improvement", "Eldritch Invocations (1 additional)"],
        13: ["Mystic Arcanum (7th-level spell, 1/day)"],
        14: ["Otherworldly Patron feature"],
        15: ["Mystic Arcanum (8th-level spell, 1/day)", "Eldritch Invocations (1 additional)"],
        16: ["Ability Score Improvement"],
        17: ["Mystic Arcanum (9th-level spell, 1/day)"],
        18: ["Eldritch Invocations (1 additional)"],
        19: ["Ability Score Improvement"],
        20: ["Eldritch Master (1/day: spend 1 min to regain all Pact Magic slots)"],
    },
    "Wizard": {
        1:  ["Spellcasting (INT-based; spellbook; ritual casting; prepare INT mod + level spells)",
             "Arcane Recovery (once/day after short rest: recover spell slots up to half wizard level)"],
        2:  ["Arcane Tradition (choose subclass)"],
        4:  ["Ability Score Improvement"],
        6:  ["Arcane Tradition feature"],
        8:  ["Ability Score Improvement"],
        10: ["Arcane Tradition feature"],
        12: ["Ability Score Improvement"],
        14: ["Arcane Tradition feature"],
        16: ["Ability Score Improvement"],
        18: ["Spell Mastery (cast 1 chosen 1st-level and 1 chosen 2nd-level spell without slots)"],
        19: ["Ability Score Improvement"],
        20: ["Signature Spells (2 chosen 3rd-level spells always prepared; cast once each/rest without a slot)"],
    },
}

# asi: [STR, DEX, CON, INT, WIS, CHA]
# Use None for scores that depend on player choice; resolved in main().
RACIAL_FEATURES = {
    "Human": {
        "asi": [1, 1, 1, 1, 1, 1],
        "speed": 30, "size": "Medium",
        "features": ["Extra Language (one additional language of your choice)"],
        "languages": ["Common", "One extra language of your choice"],
    },
    "Variant Human": {
        # Player picks any 2 different stats; each gets +1. Resolved in main().
        "asi": None,
        "speed": 30, "size": "Medium",
        "features": [
            "Skill Proficiency (choose one skill)",
            "Feat (choose one feat at 1st level)",
        ],
        "languages": ["Common", "One extra language of your choice"],
    },
    "High Elf": {
        "asi": [0, 2, 0, 1, 0, 0],
        "speed": 30, "size": "Medium",
        "features": [
            "Darkvision (60 ft.)",
            "Keen Senses (proficiency in Perception)",
            "Fey Ancestry (advantage on saves vs. charm; immune to magical sleep)",
            "Trance (4-hour rest replaces sleep; recall memories from the 4 hours vividly)",
            "Elf Weapon Training (longswords, shortswords, shortbows, longbows)",
            "Cantrip (one wizard cantrip, INT-based)",
            "Extra Language (one of your choice)",
        ],
        "languages": ["Common", "Elvish", "One extra language of your choice"],
    },
    "Wood Elf": {
        "asi": [0, 2, 0, 0, 1, 0],
        "speed": 35, "size": "Medium",
        "features": [
            "Darkvision (60 ft.)",
            "Keen Senses (proficiency in Perception)",
            "Fey Ancestry (advantage on saves vs. charm; immune to magical sleep)",
            "Trance (4-hour rest replaces sleep)",
            "Elf Weapon Training (longswords, shortswords, shortbows, longbows)",
            "Fleet of Foot (speed 35 ft.)",
            "Mask of the Wild (can Hide when lightly obscured by natural phenomena)",
        ],
        "languages": ["Common", "Elvish"],
    },
    "Drow (Dark Elf)": {
        "asi": [0, 2, 0, 0, 0, 1],
        "speed": 30, "size": "Medium",
        "features": [
            "Superior Darkvision (120 ft.)",
            "Keen Senses (proficiency in Perception)",
            "Fey Ancestry (advantage on saves vs. charm; immune to magical sleep)",
            "Trance (4-hour rest replaces sleep)",
            "Drow Weapon Training (rapiers, shortswords, hand crossbows)",
            "Drow Magic: Dancing Lights cantrip; Faerie Fire 1/day (lvl 3+); Darkness 1/day (lvl 5+) — CHA-based",
            "Sunlight Sensitivity (disadvantage on attack rolls and Perception checks in direct sunlight)",
        ],
        "languages": ["Common", "Elvish"],
    },
    "Hill Dwarf": {
        "asi": [0, 0, 2, 0, 1, 0],
        "speed": 25, "size": "Medium",
        "features": [
            "Darkvision (60 ft.)",
            "Dwarven Resilience (advantage on saves vs. poison; resistance to poison damage)",
            "Dwarven Combat Training (battleaxes, handaxes, light hammers, warhammers)",
            "Tool Proficiency (one artisan's tool of your choice)",
            "Stonecunning (double proficiency on History checks about stone/masonry origins)",
            "Dwarven Toughness (+1 maximum HP per level)",
        ],
        "languages": ["Common", "Dwarvish"],
    },
    "Mountain Dwarf": {
        "asi": [2, 0, 2, 0, 0, 0],
        "speed": 25, "size": "Medium",
        "features": [
            "Darkvision (60 ft.)",
            "Dwarven Resilience (advantage on saves vs. poison; resistance to poison damage)",
            "Dwarven Combat Training (battleaxes, handaxes, light hammers, warhammers)",
            "Tool Proficiency (one artisan's tool of your choice)",
            "Stonecunning (double proficiency on History checks about stone/masonry origins)",
            "Dwarven Armor Training (proficiency with light and medium armor)",
        ],
        "languages": ["Common", "Dwarvish"],
    },
    "Lightfoot Halfling": {
        "asi": [0, 2, 0, 0, 0, 1],
        "speed": 25, "size": "Small",
        "features": [
            "Lucky (reroll any 1 on an attack roll, ability check, or saving throw; must use new roll)",
            "Brave (advantage on saving throws against being frightened)",
            "Halfling Nimbleness (can move through the space of any larger creature)",
            "Naturally Stealthy (can hide when obscured by a creature at least one size larger)",
        ],
        "languages": ["Common", "Halfling"],
    },
    "Stout Halfling": {
        "asi": [0, 2, 1, 0, 0, 0],
        "speed": 25, "size": "Small",
        "features": [
            "Lucky (reroll any 1 on an attack roll, ability check, or saving throw; must use new roll)",
            "Brave (advantage on saving throws against being frightened)",
            "Halfling Nimbleness (can move through the space of any larger creature)",
            "Stout Resilience (advantage on saves vs. poison; resistance to poison damage)",
        ],
        "languages": ["Common", "Halfling"],
    },
    "Forest Gnome": {
        "asi": [0, 1, 0, 2, 0, 0],
        "speed": 25, "size": "Small",
        "features": [
            "Darkvision (60 ft.)",
            "Gnome Cunning (advantage on INT, WIS, and CHA saves against magic)",
            "Natural Illusionist (Minor Illusion cantrip, INT-based)",
            "Speak with Small Beasts (communicate simple ideas with Small or smaller beasts)",
        ],
        "languages": ["Common", "Gnomish"],
    },
    "Rock Gnome": {
        "asi": [0, 0, 1, 2, 0, 0],
        "speed": 25, "size": "Small",
        "features": [
            "Darkvision (60 ft.)",
            "Gnome Cunning (advantage on INT, WIS, and CHA saves against magic)",
            "Artificer's Lore (double proficiency on History checks about magical/alchemical/technological items)",
            "Tinker (proficiency with artisan's tools; build tiny clockwork devices with minor effects)",
        ],
        "languages": ["Common", "Gnomish"],
    },
    "Half-Elf": {
        # +2 CHA fixed; player picks 2 other stats for +1 each. Resolved in main().
        "asi": None,
        "speed": 30, "size": "Medium",
        "features": [
            "Darkvision (60 ft.)",
            "Fey Ancestry (advantage on saves vs. charm; immune to magical sleep)",
            "Skill Versatility (proficiency in 2 skills of your choice)",
        ],
        "languages": ["Common", "Elvish", "One extra language of your choice"],
    },
    "Half-Orc": {
        "asi": [2, 0, 1, 0, 0, 0],
        "speed": 30, "size": "Medium",
        "features": [
            "Darkvision (60 ft.)",
            "Menacing (proficiency in the Intimidation skill)",
            "Relentless Endurance (once/day: when reduced to 0 HP, drop to 1 HP instead)",
            "Savage Attacks (on a melee weapon critical hit, roll one extra damage die)",
        ],
        "languages": ["Common", "Orc"],
    },
    "Tiefling": {
        "asi": [0, 0, 0, 1, 0, 2],
        "speed": 30, "size": "Medium",
        "features": [
            "Darkvision (60 ft.)",
            "Hellish Resistance (resistance to fire damage)",
            "Infernal Legacy: Thaumaturgy cantrip; Hellish Rebuke 1/day (lvl 3+); Darkness 1/day (lvl 5+) — CHA-based",
        ],
        "languages": ["Common", "Infernal"],
    },
    "Dragonborn": {
        "asi": [2, 0, 0, 0, 0, 1],
        "speed": 30, "size": "Medium",
        "features": [
            "Draconic Ancestry (choose a dragon type; determines breath weapon damage type and resistance)",
            "Breath Weapon (action; CON save; damage scales with level: 2d6 at 1st, 3d6 at 6th, 4d6 at 11th, 5d6 at 16th; 1/rest)",
            "Damage Resistance (resistance to the damage type of your draconic ancestry)",
        ],
        "languages": ["Common", "Draconic"],
    },
}

BACKGROUNDS = {
    "Acolyte": {
        "skills": ["Insight", "Religion"],
        "tools": [], "languages": "Two languages of your choice",
        "equipment": "Holy symbol, prayer book or prayer wheel, 5 sticks of incense, vestments, common clothes, 15 gp",
        "feature": "Shelter of the Faithful: You and companions receive free healing and care at temples of your faith; clergy may provide aid (within reason).",
    },
    "Charlatan": {
        "skills": ["Deception", "Sleight of Hand"],
        "tools": ["Disguise kit", "Forgery kit"], "languages": None,
        "equipment": "Fine clothes, disguise kit, tools of your con (e.g., weighted dice, marked cards), 15 gp",
        "feature": "False Identity: You have a second identity with documentation and established history. You can also forge documents.",
    },
    "Criminal": {
        "skills": ["Deception", "Stealth"],
        "tools": ["One type of gaming set", "Thieves' tools"], "languages": None,
        "equipment": "Crowbar, dark common clothes with a hood, 15 gp",
        "feature": "Criminal Contact: A reliable contact in the criminal underworld who acts as your go-between for information and jobs.",
    },
    "Entertainer": {
        "skills": ["Acrobatics", "Performance"],
        "tools": ["Disguise kit", "One musical instrument of your choice"], "languages": None,
        "equipment": "A musical instrument, a favor from an admirer, a costume, 15 gp",
        "feature": "By Popular Demand: You can find a place to perform and receive free modest lodging and food; you may accumulate fans in that area.",
    },
    "Folk Hero": {
        "skills": ["Animal Handling", "Survival"],
        "tools": ["One type of artisan's tools", "Vehicles (land)"], "languages": None,
        "equipment": "Artisan's tools, shovel, iron pot, common clothes, 10 gp",
        "feature": "Rustic Hospitality: Common folk will shelter and protect you as one of their own (within reason), keeping your presence secret.",
    },
    "Guild Artisan": {
        "skills": ["Insight", "Persuasion"],
        "tools": ["One type of artisan's tools"], "languages": "One language of your choice",
        "equipment": "Artisan's tools, letter of introduction from your guild, traveler's clothes, 15 gp",
        "feature": "Guild Membership: Fellow guild members provide lodging and food. The guild can provide legal help and business contacts.",
    },
    "Hermit": {
        "skills": ["Medicine", "Religion"],
        "tools": ["Herbalism kit"], "languages": "One language of your choice",
        "equipment": "Scroll case with notes on your studies, winter blanket, common clothes, herbalism kit, 5 gp",
        "feature": "Discovery: You uncovered a unique and profound secret during your seclusion. Work with your DM to determine its nature.",
    },
    "Noble": {
        "skills": ["History", "Persuasion"],
        "tools": ["One type of gaming set"], "languages": "One language of your choice",
        "equipment": "Fine clothes, signet ring, scroll of pedigree, 25 gp",
        "feature": "Position of Privilege: You're welcome in high society; common folk assume you have the right to be anywhere. Others go out of their way to please you.",
    },
    "Outlander": {
        "skills": ["Athletics", "Survival"],
        "tools": ["One musical instrument of your choice"], "languages": "One language of your choice",
        "equipment": "Staff, hunting trap, trophy from an animal, traveler's clothes, 10 gp",
        "feature": "Wanderer: Excellent memory for terrain and geography; can find food and fresh water for yourself and up to 5 others in the wilderness.",
    },
    "Sage": {
        "skills": ["Arcana", "History"],
        "tools": [], "languages": "Two languages of your choice",
        "equipment": "Bottle of black ink, quill, small knife, letter from a dead colleague with an unanswered question, common clothes, 10 gp",
        "feature": "Researcher: When you don't know information, you know where and from whom to obtain it (though it may be costly or dangerous).",
    },
    "Sailor": {
        "skills": ["Athletics", "Perception"],
        "tools": ["Navigator's tools", "Vehicles (water)"], "languages": None,
        "equipment": "Belaying pin (club), 50 ft. silk rope, lucky charm, common clothes, 10 gp",
        "feature": "Ship's Passage: You can secure free passage on sailing ships for yourself and companions in exchange for labor.",
    },
    "Soldier": {
        "skills": ["Athletics", "Intimidation"],
        "tools": ["One type of gaming set", "Vehicles (land)"], "languages": None,
        "equipment": "Insignia of rank, trophy from a fallen enemy, deck of cards or dice, common clothes, 10 gp",
        "feature": "Military Rank: Soldiers of your old army recognize your rank and defer to you. You can commandeer equipment and personnel for temporary use.",
    },
    "Urchin": {
        "skills": ["Sleight of Hand", "Stealth"],
        "tools": ["Disguise kit", "Thieves' tools"], "languages": None,
        "equipment": "Small knife, map of the city you grew up in, token from your parents, common clothes, 10 gp",
        "feature": "City Secrets: You know the city's secret passages and back alleys. You and companions move at twice normal speed when not in combat in a city.",
    },
}

# --- Utility Functions ---

def modifier(score):
    return (score - 10) // 2

def mod_str(mod):
    return f"+{mod}" if mod >= 0 else str(mod)

def asi_description(asi):
    """Build a human-readable ASI string from the [STR,DEX,CON,INT,WIS,CHA] list."""
    parts = [f"+{asi[i]} {STATS[i]}" for i in range(6) if asi[i] != 0]
    return ", ".join(parts) if parts else "None"

def calculate_hp(char_class, level, con_mod):
    hit_die = HIT_DICE[char_class]
    avg = (hit_die // 2) + 1  # average rounded up for levels 2+
    hp = hit_die + con_mod   # level 1 is always max die
    for _ in range(level - 1):
        hp += avg + con_mod
    return max(hp, level)    # minimum 1 HP per level

def choose_from(prompt, options):
    print(f"\n  Options: {', '.join(options)}")
    while True:
        choice = input(f"  {prompt}: ").strip()
        match = next((o for o in options if o.lower() == choice.lower()), None)
        if match:
            return match
        print("  Not recognized. Please choose from the list above.")

def get_int(prompt, lo=1, hi=20):
    while True:
        try:
            val = int(input(f"  {prompt}: ").strip())
            if lo <= val <= hi:
                return val
            print(f"  Enter a number between {lo} and {hi}.")
        except ValueError:
            print("  Please enter a whole number.")

def get_ability_scores():
    print("\nAbility Scores (enter base scores before racial bonuses):")
    return {stat: get_int(stat, 1, 30) for stat in STATS}

def resolve_racial_asi(race):
    """
    For races with player-choice ASIs (Variant Human, Half-Elf), prompt the user
    and return a resolved [STR, DEX, CON, INT, WIS, CHA] bonus list.
    For all other races, return the fixed list directly.
    """
    asi = RACIAL_FEATURES[race]["asi"]
    if asi is not None:
        return list(asi)

    bonus = [0, 0, 0, 0, 0, 0]

    if race == "Variant Human":
        print("\nVariant Human: choose 2 different ability scores to each receive +1.")
        chosen = []
        for n in ("first", "second"):
            remaining = [s for s in STATS if s not in chosen]
            stat = choose_from(f"  {n.capitalize()} stat (+1)", remaining)
            bonus[STATS.index(stat)] += 1
            chosen.append(stat)

    elif race == "Half-Elf":
        print("\nHalf-Elf: +2 CHA is fixed. Choose 2 other ability scores to each receive +1.")
        bonus[STATS.index("CHA")] = 2
        chosen = []
        for n in ("first", "second"):
            remaining = [s for s in STATS if s != "CHA" and s not in chosen]
            stat = choose_from(f"  {n.capitalize()} stat (+1)", remaining)
            bonus[STATS.index(stat)] += 1
            chosen.append(stat)

    return bonus

# --- Display ---

def display(name, race, char_class, level, background, base_scores, asi):
    # Apply racial bonuses
    final_scores = {stat: base_scores[stat] + asi[i] for i, stat in enumerate(STATS)}

    prof = PROFICIENCY_BONUS[level]
    con_mod = modifier(final_scores["CON"])
    hp = calculate_hp(char_class, level, con_mod)
    race_data = RACIAL_FEATURES[race]
    cp = CLASS_PROFICIENCIES[char_class]
    bg = BACKGROUNDS[background]

    W = 62
    print("\n" + "=" * W)
    print(f"  {name}")
    print(f"  Level {level} {race} {char_class}  |  Background: {background}")
    print("=" * W)

    # Ability scores
    print("\nABILITY SCORES")
    for i, stat in enumerate(STATS):
        base  = base_scores[stat]
        bonus = asi[i]
        final = final_scores[stat]
        mod   = modifier(final)
        if bonus != 0:
            print(f"  {stat}: {base} + {bonus} (racial) = {final}  ({mod_str(mod)})")
        else:
            print(f"  {stat}: {final}  ({mod_str(mod)})")

    # Core stats
    print("\nCORE STATS")
    print(f"  Hit Points : {hp}  (d{HIT_DICE[char_class]} hit die × {level} levels)")
    print(f"  Speed      : {race_data['speed']} ft.")
    print(f"  Size       : {race_data['size']}")
    print(f"  Prof. Bonus: {mod_str(prof)}")

    # Proficiencies
    print("\nPROFICIENCIES")
    print(f"  Saving Throws : {', '.join(cp['saving_throws'])}")
    print(f"  Armor         : {', '.join(cp['armor']) if cp['armor'] else 'None'}")
    print(f"  Weapons       : {', '.join(cp['weapons'])}")
    if cp["tools"]:
        print(f"  Tools (class) : {', '.join(cp['tools'])}")
    if bg["tools"]:
        print(f"  Tools (bg)    : {', '.join(bg['tools'])}")
    print(f"  Class Skills  : {cp['skills']}")
    print(f"  BG Skills     : {', '.join(bg['skills'])}")

    # Languages
    langs = list(race_data["languages"])
    if bg["languages"]:
        langs.append(bg["languages"])
    print("\nLANGUAGES")
    for lang in langs:
        print(f"  - {lang}")

    # Racial features
    print(f"\nRACIAL FEATURES  [{race}]")
    print(f"  Ability Score Increases: {asi_description(asi)}")
    for feat in race_data["features"]:
        print(f"  - {feat}")

    # Class features
    print(f"\nCLASS FEATURES  [{char_class}, Levels 1\u2013{level}]")
    feats_by_level = CLASS_FEATURES[char_class]
    shown_any = False
    for lvl in range(1, level + 1):
        for feat in feats_by_level.get(lvl, []):
            prefix = f"  [Lv {lvl:2}] " if not feat.startswith("  ") else "          "
            print(f"{prefix}{feat.strip()}")
            shown_any = True
    if not shown_any:
        print("  (No features recorded for this level range)")

    # Background feature
    print(f"\nBACKGROUND FEATURE  [{background}]")
    print(f"  {bg['feature']}")
    print(f"\n  Starting Equipment: {bg['equipment']}")

    print("\n" + "=" * W)

# --- Main ---

def main():
    W = 62
    print("=" * W)
    print("         D&D 5E \u2014 CHARACTER ABILITIES SUMMARY")
    print("=" * W)

    name = input("\nCharacter name (or press Enter for 'Unnamed'): ").strip() or "Unnamed"

    print("\nRace")
    race = choose_from("Choose race", list(RACIAL_FEATURES.keys()))

    print("\nClass")
    char_class = choose_from("Choose class", list(HIT_DICE.keys()))

    print("\nLevel")
    level = get_int("Level (1\u201320)", 1, 20)

    print("\nBackground")
    background = choose_from("Choose background", list(BACKGROUNDS.keys()))

    base_scores = get_ability_scores()

    asi = resolve_racial_asi(race)

    display(name, race, char_class, level, background, base_scores, asi)

if __name__ == "__main__":
    main()
