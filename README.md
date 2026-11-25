# Awesome Unreal Engine Game Templates, Blueprints & Pro Open-Source Frameworks

A massive, categorized catalog of **Unreal Engine 5 (UE 5.x–5.8)** game templates, Blueprint kits, official Epic samples, and production-grade free & open-source frameworks across every major game genre and engine subsystem.

> **Note on versions & licenses:** UE4 / UE 5.0–5.5 Blueprint projects typically upgrade cleanly to UE 5.8; C++ plugins/projects may require minor API updates on compile. Always check each repository's `LICENSE` before shipping a closed-source commercial game (GPL-2.0/3.0 repos are marked explicitly).

---

## Table of Contents

1. [Official Epic Games Built-In Templates & Free Fab Samples](#1-official-epic-games-built-in-templates--free-fab-samples)
2. [Production-Grade Free & Open-Source Core Frameworks](#2-production-grade-free--open-source-core-frameworks)
3. [FPS, Arena, Tactical & Extraction Shooters](#3-fps-arena-tactical--extraction-shooters)
4. [Third-Person Action, Souls-like, Stealth, Parry & Fighting](#4-third-person-action-souls-like-stealth-parry--fighting)
5. [Action RPG, Top-Down ARPG (Diablo-like), cRPG & Roguelikes](#5-action-rpg-top-down-arpg-diablo-like-crpg--roguelikes)
6. [MOBA & Hero Arena](#6-moba--hero-arena)
7. [Inventory, Equipment, Quests, Dialogue & Visual Novels](#7-inventory-equipment-quests-dialogue--visual-novels)
8. [Survival, Crafting, Base Building & Horror](#8-survival-crafting-base-building--horror)
9. [Locomotion, Animation, Parkour & Secondary Hair/Cloth Physics](#9-locomotion-animation-parkour--secondary-haircloth-physics)
10. [Modular Character Creators, Mutable (UE 5.8), Runtime glTF/VRM & Facial Mocap](#10-modular-character-creators-mutable-ue-58-runtime-gltfvrm--facial-mocap)
11. [Platformer, Side-Scroller, Metroidvania & 2D / 2.5D](#11-platformer-side-scroller-metroidvania--2d--25d)
12. [RTS, Turn-Based Strategy, Tower Defense & City/Farm Builders](#12-rts-turn-based-strategy-tower-defense--cityfarm-builders)
13. [Racing, Vehicles, 6DOF Space Flight & Drone Simulators](#13-racing-vehicles-6dof-space-flight--drone-simulators)
14. [Card Games, Board Games & Puzzles](#14-card-games-board-games--puzzles)
15. [Multiplayer, Party, Co-op, Online Services (OSSv2/Steam/PlayFab) & MMO Backends](#15-multiplayer-party-co-op-online-services-ossv2steamplayfab--mmo-backends)
16. [VR / XR / AR](#16-vr--xr--ar)
17. [Portals, Physics Sandboxes, Chaos Destruction & Level Builders](#17-portals-physics-sandboxes-chaos-destruction--level-builders)
18. [AI, StateTree, 3D Navigation & Mass Entity Crowds](#18-ai-statetree-3d-navigation--mass-entity-crowds)
19. [World, PCG (UE 5.8), Weather, GPU Water, Foliage & 3D Gaussian Splatting](#19-world-pcg-ue-58-weather-gpu-water-foliage--3d-gaussian-splatting)
20. [Stylized / Anime Toon Rendering & Audio / MetaSounds DSP](#20-stylized--anime-toon-rendering--audio--metasounds-dsp)
21. [UI, Settings Menus, Loading Screens, Pooling, Validation, Telemetry & Testing](#21-ui-settings-menus-loading-screens-pooling-validation-telemetry--testing)
22. [Commercial / Pro Fab Frameworks (Reference)](#22-commercial--pro-fab-frameworks-reference)
23. [Giant Indexes, Blueprint Paste-Bins & Free Hubs](#23-giant-indexes-blueprint-paste-bins--free-hubs)
24. [Recommended Commercial-Safe Open-Source Stack (MIT / Apache-2.0)](#24-recommended-commercial-safe-open-source-stack-mit--apache-20)

---

## 1. Official Epic Games Built-In Templates & Free Fab Samples

### Built-In UE 5.8 Templates & Genre Variant Packs
Included offline in every Unreal Engine 5.8 installation under `<UE_5.8>/Templates/` (`FeaturePacks/*.upack` and `TemplateResources/Standard/Variant_*`):
- **Core Templates:** `TP_FirstPersonBP`, `TP_ThirdPersonBP`, `TP_TopDownBP`, `TP_VehicleAdvBP`, `TP_VirtualRealityBP`, `TP_HandheldARBP`
- **9 Built-In Genre Variant Packs:** `Variant_Combat`, `Variant_Shooter`, `Variant_Horror`, `Variant_Platforming`, `Variant_SideScroller`, `Variant_TwinStick`, `Variant_Strategy`, `Variant_Offroad`, `Variant_Timetrial`
- **Reference:** [Templates Reference](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-templates-reference) · [Samples & Tutorials](https://dev.epicgames.com/documentation/unreal-engine/samples-and-tutorials-for-unreal-engine)

### Official Free Epic Games Samples (Fab)

| Project | Focus | Link |
|---|---|---|
| **Lyra Starter Game** | Modular multiplayer FPS/TPS, GAS, CommonUI, GameFeatures | [Fab](https://www.fab.com/listings/93faede1-4434-47c0-85f1-bf27c0820ad0) · [Docs](https://dev.epicgames.com/documentation/unreal-engine/lyra-sample-game-in-unreal-engine) |
| **Game Animation Sample (GASP)** | Motion Matching, Choosers, traversal/parkour, modular AnimBPs | [Fab](https://www.fab.com/listings/880e319a-a59e-4ed2-b268-b32dac7fa016) |
| **Stack-O-Bot** | Third-person Blueprint platformer/puzzle (rebuilt for UE 5.6+) | [Fab](https://www.fab.com/listings/b4dfff49-0e7d-4c4b-a6c5-8a0315831c9c) · [Docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/stack-o-bot-sample-game-in-unreal-engine?application_version=5.7) |
| **Cropout Sample Project** | Cross-platform top-down Casual RTS (Blueprints + CommonUI) | [Fab](https://www.fab.com/listings/bd733d81-7c29-44fe-b53f-65b14d06a9e2) · [Overview](https://www.unrealengine.com/blog/cropout-casual-rts-game-sample-project) |
| **Action RPG** | Official C++/Blueprint Action RPG (GAS, inventory, melee, save/load) | [Fab](https://www.fab.com/listings/ef04a196-03c1-4204-998a-c7d5264fade7) |
| **Multiplayer Shootout** | Official multiplayer lobby, matchmaking, and arena shootout Blueprints | [Fab](https://www.fab.com/listings/4d9fddcd-2c92-4d08-b359-ba4b0568fdfa?lang=en) |
| **Content Examples** | Per-feature Blueprint, Anim, Niagara, Material, and UMG showcase maps | [Fab](https://www.fab.com/listings/4d251261-d98c-48e2-baee-8f4e47c67091) · [Docs](https://dev.epicgames.com/documentation/unreal-engine/content-examples-sample-project-for-unreal-engine?lang=en-US) |
| **Epic Blueprints Showcase** | Level design tools, security systems, and AI Blueprint demos | [Fab](https://www.fab.com/listings/720af3f1-cd24-40a3-a881-ee695a7c9779?lang=en) |
| **A-COM Animation Sample** | Stylized biped & quadruped animation rigs/blueprints | [Fab](https://www.fab.com/listings/7a019296-852d-47b8-86ed-ddcf2835a352?lang=en) |
| **City Sample / Electric Dreams / Valley of the Ancient** | Open-world traffic/crowds, PCG, Substrate, Nanite/Lumen showcases | [Feature Examples](https://dev.epicgames.com/documentation/unreal-engine/engine-feature-examples-for-unreal-engine) · [Sample Games](https://dev.epicgames.com/documentation/unreal-engine/sample-game-projects-for-unreal-engine) |

---

## 2. Production-Grade Free & Open-Source Core Frameworks

| Framework | License | UE / Stack | What It Gives You | Link |
|---|---|---|---|---|
| **Omega Game Framework** | MIT | UE5 · C++/BP | Modular RPG/action framework: abilities, attributes, XP, turn order, inventory, equipment, save system, zone manager, FlowGraph integration | [GitHub](https://github.com/StudioSyndiCatCaius/OmegaGameFramework) · [Fab](https://www.fab.com/listings/1e72596a-b243-43b8-a6f2-b972570fb5f8?lang=en) · [Basic Template](https://www.fab.com/listings/59e40fc2-4d7b-4edf-8722-184da669a160) |
| **AyaDogGames GameplayFramework** | Apache-2.0 | UE 5.7 · C++/BP | Replicated data-driven GAS framework: `AbilitySet`/`PawnData`, CommonUI + MVVM, tag-mapped Enhanced Input, `FFastArraySerializer` inventory, AI/item spawners | [GitHub](https://github.com/AyaDogGames/GameplayFramework) |
| **GameCoreFramework (GCF)** | Open Source | UE5 · C++/BP | Lyra-inspired modular multiplayer framework with Dual ASC architecture, input routing, tickless event-driven design | [GitHub](https://github.com/asugeno/GameCoreFramework) |
| **XistCommonGameSample** | MIT | UE 5.7 · C++/BP | Clean single-player stripped setup of Lyra's `CommonGame`, `CommonUser`, `GameplayMessageRouter`, and `ModularGameplayActors` plugins | [GitHub](https://github.com/XistGG/XistCommonGameSample) |
| **ArtilleryEco** *(pre-alpha)* | MIT | UE5 · C++ | Off-game-thread deterministic gameplay & ability simulation backed by Jolt Physics (Barrage) and input-stream replication (Bristlecone) | [GitHub](https://github.com/OversizedSunCoreDev/ArtilleryEco) |
| **OpenUnrealUtilities (OUU)** | Open Source | UE4/5 · C++/BP | Studio-proven general-purpose Unreal C++/Blueprint utilities plugin | [GitHub](https://github.com/JonasReich/OpenUnrealUtilities) |
| **Unreal Angelscript** | Open Source | UE5 · C++ | Hazelight Studios' hot-reloading gameplay scripting language (vanilla engine plugin port) | [Docs](https://github.com/Hazelight/Docs-UnrealEngine-Angelscript) · [Plugin Port](https://github.com/WillGordon9999/UE-Angelscript) |
| **EssentialUE5BPs** | Open Source | UE5 · BP | Modular third-person Blueprints collection | [GitHub](https://github.com/lostcrowdev/EssentialUE5BPs) |
| **UE5 Game Starter Template** | Open Source | UE5 | General-purpose project starter | [GitHub](https://github.com/motionforge/Unreal-Engine-5-Game-Starter-Template) |
| **Nano** | Open Source | UE | Minimalist starter template for small/jam games | [GitHub](https://github.com/pfist/Nano) |

---

## 3. FPS, Arena, Tactical & Extraction Shooters

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **GASShooter (UE 5.5)** | GitHub | UE 5.5 · MIT | Full multiplayer FPS/TPS built on Gameplay Ability System | [GitHub](https://github.com/pikogoro/GASShooter_UE55) |
| **GASShooter (Original)** | GitHub | UE4/5 · MIT | Canonical GAS shooter reference | [GitHub](https://github.com/tranek/GASShooter) |
| **Realistic Assault Rifle Template** | GitHub | UE5 · BP | Modular weapon attachments, animations, FPS Blueprint system | [GitHub](https://github.com/OctavianTocan/Realistic-Assault-Rifle-Template) |
| **Unreal Shooter Base** | GitHub | UE5 · C++/BP | Multiplayer shooter w/ GAS, AI Behavior Trees, networked physics | [GitHub](https://github.com/SucceedHQ-innovations/unreal-shooter-base) |
| **SuperSimpleFPSPack** | GitHub | UE 5.5 · BP | Extended First Person Shooter starter | [GitHub](https://github.com/KPettingerEEN/SuperSimpleFPSPack) |
| **UE5 Arena Shooter Sample** | GitHub | UE5 · C++ | Arena / boomer shooter movement & combat | [GitHub](https://github.com/KamikaziUk/UE5-Arena-Shooter-Sample) |
| **Blackline Contract (PTA)** | GitHub | UE 5.5 | Tactical extraction shooter prototype | [GitHub](https://github.com/triopstudios/blacklinecontract_pta) |
| **UE5 Weapon System** | GitHub | UE5 · BP/C++ | Projectiles, muzzle flash, bullet hole decals, impact VFX | [GitHub](https://github.com/ArtemChig/UE5-Weapon-System) |
| **UE5-EnhancedProjectile** | GitHub | UE5 · C++/BP | StateTree-driven projectile framework with pooling & prediction validation | [GitHub](https://github.com/HanYe0817/UE5-EnhancedProjectile) |
| **SimpleFPSTemplate** | GitHub | UE4/5 · C++ | Minimalist FPS starter by Tom Looman | [GitHub](https://github.com/tomlooman/SimpleFPSTemplate) |
| **Kosm Classic FPS Template** | GitHub | UE4 · BP | Classic arena shooter mechanics & pickups | [GitHub](https://github.com/vtx-factory/Kosm-Classic-FPS-Template-UE4) |
| **Project Isolation** | GitHub | UE · MIT | Open-source single-player FPS C++ codebase | [GitHub](https://github.com/whoisEllie/Project-Isolation) |
| **Free FPS Template & Tutorial** | Fab | UE5 · Free | Free starter FPS Blueprint project & tutorial | [Fab](https://www.fab.com/listings/6a0af880-2b74-480c-a82c-8e597918dffe?lang=en) |
| **Realistic FP Movement V1** | itch.io | UE5 · Free | Free realistic first-person movement template | [itch.io](https://treetygames.itch.io/realistic-first-person-movement-template-v1-in-unreal-engine-5-free-download) |

---

## 4. Third-Person Action, Souls-like, Stealth, Parry & Fighting

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **CoopSoulsGame (UE 5.7)** | GitHub | UE 5.7 · C++/BP | Light/heavy/charge attacks, parry, dodge, backstab, poise, boss AI, lock-on | [GitHub](https://github.com/Roomixer/Souls-game-UE-5.7) |
| **Sekiro Clone (Action Adventure)** | GitHub | UE5 · C++ (GAS) | Deflect/parry, posture stagger, backstab & plunging deathblows, grappling hook, wall jump, stealth whistle, lock-on | [GitHub](https://github.com/kantam5/UE5-Action-Adventure-Sekiro-Clone) |
| **StealthDemo** | GitHub | UE 5.5 · C++ | Third-person stealth action: AI security cameras, patrol robots, Attack ↔ Search ↔ Patrol Behavior Trees | [GitHub](https://github.com/CanReader/StealthDemo) |
| **UE5 RPG Melee Combat System** | GitHub | UE5 · C++/BP | Modular melee combat: combo windows, input buffering, anim-driven hit detection | [GitHub](https://github.com/Mustafa-Kum/ue5-rpg-melee-combat-system) |
| **UE5 Soulslike Combat** | GitHub | UE 5.7 | Souls-like combat project | [GitHub](https://github.com/Kulahala/UE5-Soulslike-Combat) |
| **Soulsborne** | GitHub | UE5 | Third-person Souls-like project | [GitHub](https://github.com/St4rman/Soulsborne) |
| **Echoes of the Lost Sands** | GitHub | UE5 | Souls-like RPG with melee combat & AI enemies | [GitHub](https://github.com/Mecha-NOX/Echoes-of-the-Lost-Sands) |
| **MedivalCombatGame** | GitHub | UE5 · C++ | Souls-inspired medieval combat prototype | [GitHub](https://github.com/KevinRusev/MedivalCombatGame) |
| **UE5 Hack and Slash** | GitHub | UE5 · GPL-3.0 | Third-person hack & slash action game | [GitHub](https://github.com/willroberts/ue5-hack-and-slash) |
| **NightSkyEngine** | GitHub | UE · MIT | C++ fighting-game framework | [GitHub](https://github.com/WistfulHopes/NightSkyEngine) |
| **TargetSystemPlugin** | GitHub | UE4/5 | Dark Souls-style camera lock-on / targeting plugin | [GitHub](https://github.com/mklabs/ue4-targetsystemplugin) |
| **WeaponTrace-Unreal** | GitHub | UE · Plugin | Reliable melee weapon socket/sweep hit tracing | [GitHub](https://github.com/getnamo/WeaponTrace-Unreal) |
| **Enhanced Third Person Template** | Fab | UE5 · BP | Modernized drop-in third-person starter | [Fab](https://www.fab.com/listings/90517cb6-120b-4d8c-b8b3-1f9a74b91104?lang=en) |

---

## 5. Action RPG, Top-Down ARPG (Diablo-like), cRPG & Roguelikes

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **ActionRoguelike (Tom Looman)** | GitHub | UE5 · C++/BP | Co-op action roguelike: abilities, AI, items, multiplayer (4.5k+★) | [GitHub](https://github.com/tomlooman/ActionRoguelike) |
| **Obsidian** | GitHub | UE5 · GPL-3.0 | Multiplayer Diablo-2-style GAS ARPG: procedural loot/affixes, replicated grid inventory, equipment mesh spawning, stash tabs, boss AI | [GitHub](https://github.com/intrxx/Obsidian) |
| **CharmingCraft** | GitHub | UE 5.3 · GPL-2.0 | Top-down low-poly RPG (Minecraft Dungeons / Albion Online): GAS item skills, modular armor/weapon assembly, chunks, farming & building | [GitHub](https://github.com/Caishangqi/CharmingCraft) |
| **UE5TopDownARPG** | GitHub | UE5 · C++/BP | Clean top-down ARPG starter (Ubisoft Sofia / Univ. of Sofia architecture course) | [GitHub](https://github.com/k1p1/UE5TopDownARPG) |
| **cRPG-Project** | GitHub | UE5 · C++/BP | Multiplayer turn-based cRPG: data-driven Gameplay Action System, encounter manager, inventory, DFS GOAP AI | [GitHub](https://github.com/e-oneill/cRPG-Project) |
| **ActionRPG-UE5** | GitHub | UE5 · C++/BP | Epic's official ActionRPG sample upgraded to UE5 | [GitHub](https://github.com/BoilTask/ActionRPG-UE5) |
| **ActionRPGV5** | GitHub | UE5 · MIT | Clean Action RPG sample for UE5 | [GitHub](https://github.com/dahlgrenmartin/ActionRPGV5) |
| **Open RPG Template** | GitHub | UE 5.4 · MIT | Open-source RPG starter template | [GitHub](https://github.com/polygonvariable/open-rpg-template) |
| **RPGTemplate** | GitHub | UE5 | Modular RPG project template | [GitHub](https://github.com/eren-pekdemir/RPGTemplate) |
| **ParagonGAS** | GitHub | UE5 · GAS | GAS combat system using free Fab Paragon assets | [GitHub](https://github.com/realchrisparker/ParagonGAS) |
| **UE5 C++ GAS Code Samples** | GitHub | UE5 · C++ | GAS abilities, attributes, effects, AI & RPG progression | [GitHub](https://github.com/jessebr2/UE5-Cpp-GAS-Code-Samples) |
| **GASDocumentation** | GitHub | UE4/5 · MIT | Definitive GAS documentation + multiplayer sample project | [GitHub](https://github.com/tranek/GASDocumentation) |
| **Solo-Leveling-ARPG** | GitHub | UE 5.7.2 · C++ | Large ARPG foundation: procedural dungeons (10 biomes / 6 ranks), world events, quests, guilds, NPC schedules (WIP) | [GitHub](https://github.com/clarkstone/Solo-Leveling-ARPG) |

---

## 6. MOBA & Hero Arena

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **Tartarus Arena** | GitHub | **UE 5.8** · MIT | Full 5v5 MOBA (Smite-style Arena + 3-lane Conquest), GAS, 11 Paragon hero configs, 27-item shop, smart bots, LAN multiplayer, plus a Hades-style action prototype | [GitHub](https://github.com/BartekZawadzki/TartarusArena) |

---

## 7. Inventory, Equipment, Quests, Dialogue & Visual Novels

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **InventoryPluginUE5** | GitHub | UE 5.6+ · MIT | Server-authoritative multiplayer spatial-grid inventory (`FInv_ItemFragment` + `FFastArraySerializer`), drag-drop UI, equipment socket spawning, weight system | [GitHub](https://github.com/alessandrobelli/InventoryPluginUE5) |
| **UE5 RPG Inventory System** | GitHub | UE5 · GAS/UI | Modular inventory, equipment stats & modular mesh swapping | [GitHub](https://github.com/Mustafa-Kum/ue5-rpg-inventory-system) |
| **InventorySystem (Hotbar)** | GitHub | UE5 · BP | Easy hotbar & inventory system | [GitHub](https://github.com/finalstack/InventorySystem) |
| **Free Modular List Inventory** | Fab | UE5 · Free | Free modular list inventory Blueprint system | [Fab](https://www.fab.com/listings/e28df43c-6ed8-4616-9d02-0fa3756f39f8?lang=en) |
| **Mountea Framework Suite** | GitHub | UE5 · MPL-2.0 / GPL-2.0 | Dialogue Tree editor + validator (MPL-2.0), Interaction System, Inventory & Equipment with visual slots (GPL-2.0) | [Org](https://github.com/Mountea-Framework) · [Dialogue](https://github.com/Mountea-Framework/MounteaDialogueSystem) · [Interaction](https://github.com/Mountea-Framework/MounteaInteractionSystem) · [Inventory](https://github.com/Mountea-Framework/MounteaInventoryEquipment) |
| **FlowGraph (MothCocoon)** | GitHub | UE5 · MIT | Production node-based narrative, quest & event scripting graph (1.8k+★) | [GitHub](https://github.com/MothCocoon/FlowGraph) |
| **SUQS** | GitHub | UE4/5 · MIT | Steve's data-driven Unreal Quest System | [GitHub](https://github.com/sinbad/SUQS) |
| **ArcActivities** | GitHub | UE5 | Custom graph editor for quests & gameplay activities | [GitHub](https://github.com/punyhumangames/ArcActivities) |
| **DlgSystem (NotYetGames)** | GitLab | UE4/5 · MIT | Graph-based branching dialogue plugin | [GitLab](https://gitlab.com/NotYetGames/DlgSystem) |
| **OpenRPG Modules** | GitHub | UE4/5 · BP | Modular Inventory, Quests, Stats, and 360° Radar | [Inventory](https://github.com/angelhodar/OpenRPG_Inventory) · [Quests](https://github.com/angelhodar/OpenRPG_Quest) · [Stats](https://github.com/angelhodar/OpenRPG_Stats) · [Radar](https://github.com/angelhodar/OpenRPG_RadarSystem) |
| **Shiden Visual Novel Editor** | GitHub | **UE 5.3–5.8** · MIT | Complete VN/narrative editor with live preview, 41 commands, branching, save/load, backlog, gallery, CSV/JSON I/O | [GitHub](https://github.com/HANON-games/Shiden) |
| **KaedeVN** | GitHub | **UE 5.8** · MIT | Script-driven visual novel runtime (Slate UI, KSC VM, shaders, sample 2D novel) | [GitHub](https://github.com/kaedeasset/kaedevn) |

---

## 8. Survival, Crafting, Base Building & Horror

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **DyingCity** | GitHub | **UE 5.8** · C++ | Modular survival: AI, combat, inventory, dynamic world | [GitHub](https://github.com/HideInFade/DyingCity) |
| **ALIS** | GitHub | UE5 · C++ | Open-source survival game, modular plugins, JSON data-driven architecture | [GitHub](https://github.com/fallintodusk/alis) |
| **BiomeSurvivor** | GitHub | UE5 · Co-op | Open-world multiplayer survival: biomes, crafting, building, weather, LAN/co-op | [GitHub](https://github.com/KasparPlaas/BiomeSurvivor) |
| **Survival Prototype UE5** | GitHub | UE5 · BP | Blueprint interaction, inventory, and equipment handling | [GitHub](https://github.com/vatsalmandali/survival-prototype-ue5) |
| **EpicSurvivalGame** | GitHub | UE4/5 · MIT | Classic third-person survival reference (3.3k+★) | [GitHub](https://github.com/tomlooman/EpicSurvivalGame) |
| **Survival Horror Game Template** | GitHub | UE 5.6 | Starter survival horror project | [GitHub](https://github.com/TirdadMH/Survival-Horror-Game-Template) |
| **SurvivalHorrorProject** | GitHub | UE5 | 9 environmental puzzles, per-limb hit reactions, map & inventory | [GitHub](https://github.com/andrewRCr/SurvivalHorrorProject) |
| **Forest of Nightmares** | GitHub | UE5 · C++ | Cinematic horror survival with Lumen, Nanite & VSM | [GitHub](https://github.com/hunterleek/ForestOfNightmares) |
| **BloodMoon** | GitHub | UE5 · MIT | Third-person zombie survival shooter | [GitHub](https://github.com/FreshBakedCode/BloodMoon_Public) |
| **HordeTemplate** | GitHub | UE · MIT | Wave-based horde survival template | [GitHub](https://github.com/DasBander/HordeTemplate) |
| **Budget-Backrooms** | GitHub | UE · GPL-3.0 | Single-player Backrooms atmospheric horror | [GitHub](https://github.com/dabardibid/Budget-Backrooms) |
| **FREE Complete Horror Template** | Fab | UE5 · Free | Free horror jumpstart template | [Fab](https://www.fab.com/listings/e7196401-afca-474d-88b8-537606c8c1ad?lang=en) |
| **Free Horror Game Template [UE5]** | itch.io | UE5 · Free | Free downloadable UE5 horror template | [itch.io](https://visq.itch.io/free-horror-game-template-ue5) |

---

## 9. Locomotion, Animation, Parkour & Secondary Hair/Cloth Physics

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **ALS-Refactored** | GitHub | UE5 · MIT | Production C++ rewrite of Advanced Locomotion System V4 | [GitHub](https://github.com/Sixze/ALS-Refactored) |
| **GASP-ALS-R** | GitHub | UE5 · MIT | Epic Motion Matching (GASP) + ALS-Refactored layering + GAS | [GitHub](https://github.com/SAM-tak/GASP-ALS-R) |
| **GASPALS** | GitHub | UE5 | GASP + ALS animation layering (1.1k+★) | [GitHub](https://github.com/PolygonHive/GASPALS) |
| **ALSXT** | GitHub | UE5 · Dual License | Extends `ALS-Refactored` into a modular GAS data-oriented character system | [GitHub](https://github.com/Voidware-Prohibited/ALSXT) |
| **ALS-Refactored-EOS** | GitHub | UE5 | Template combining ALS-Refactored + EOS + Steam + CommonUI | [GitHub](https://github.com/delebash/ALS-Refactored-EOS) |
| **GMCLocomotion** | GitHub | UE5 | General Movement Component + GASP Motion Matching & Warping | [GitHub](https://github.com/Dr-Rank/GMCLocomotion) |
| **MovementExhibition** | GitHub | UE5 · C++ | Replicated CharacterMovementComponent extension: grapple hook, rope, dive roll/dash, ramp physics sliding | [GitHub](https://github.com/zSelimReborn/MovementExhibition) |
| **Parkour & Climbing Systems** | GitHub | UE5 · C++/BP | Vaulting, ledge climbing, wall traversal | [C++ Parkour](https://github.com/RahulChandra99/ue5-cpp-parkour-climbing-mechanics) · [UE5ParkourSystem](https://github.com/peilunnn/UE5ParkourSystem) · [QGDeep Parkour](https://github.com/QGDeep/Parkour-System) |
| **Spider Procedural Locomotion** | GitHub | UE5 · Control Rig | Procedural multi-limb wall/ceiling locomotion | [GitHub](https://github.com/SupernerdX/UE5-Spider-Procedural-Locomotion) |
| **KawaiiPhysics** | GitHub | UE4/5 · MIT | Secondary AnimGraph bone physics for hair, skirts, sleeves, capes, and accessories | [GitHub](https://github.com/pafuhana1213/KawaiiPhysics) |
| **MallangPhysics** | GitHub | **UE 5.6–5.8** · MIT | GPU soft-body deformation on skeletal & static meshes | [GitHub](https://github.com/wjsekrud/MallangPhysics) |
| **ACL Plugin** | GitHub | UE4/5 · MIT | Animation Compression Library plugin (higher precision, lower RAM) | [GitHub](https://github.com/nfrechette/acl-ue4-plugin) |

---

## 10. Modular Character Creators, Mutable (UE 5.8), Runtime glTF/VRM & Facial Mocap

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **glTFRuntime** | GitHub | UE5 · MIT | Load `.glb`/`.gltf` meshes, skeletons, morph targets & animations **at runtime** for swappable modular limbs, outfits & hair | [GitHub](https://github.com/rdeioris/glTFRuntime) · [Docs](https://github.com/rdeioris/glTFRuntime-docs) |
| **Mutable Graph Toolset** | GitHub / Fab | **UE 5.8** | 22 native MCP tools to build Epic **Mutable** Customizable Object graphs (clothing, hair/grooms, body options), compile & preview | [GitHub](https://github.com/ITemre/MutableGraphToolset) · [Fab](https://www.fab.com/listings/aa935747-f923-4d4f-aa23-1b2a8e8a196d) |
| **FORMA Lite** | GitHub (Docs) | **UE 5.8** · BP | Blueprint character creator studio built on Mutable with third-person gameplay handoff (docs repo; project on Fab) | [GitHub](https://github.com/ITemre/FORMA-Lite) |
| **Project Phoenix (RTFKT)** | GitHub | UE5 · MIT | Open-source UE5 modular trait & wearable equip/edit studio + lighting maps | [GitHub](https://github.com/RTFKT-Ltd/ProjectPhoenix-UE5) |
| **VRM4U** | GitHub | UE5 · MIT | Runtime VRM anime character importer (skeleton retarget, spring bones, morphs, toon shaders) | [GitHub](https://github.com/ruyo/VRM4U) |
| **ue5-mmd-toolkit (AMAP5 V2)** | GitHub | UE5 | PMX/VMD model & motion pipeline generating native UE5 Skeletal Meshes and AnimSequences | [GitHub](https://github.com/AMAP-N/ue5-mmd-toolkit) |
| **unreal-audio2lipsync** | GitHub | UE5 | Audio-driven lipsync (HuBERT + Transformer → 52 ARKit blendshapes via LiveLink) | [GitHub](https://github.com/aaryansachdeva/unreal-audio2lipsync) |
| **unreal-motion (MediaPipe4U)** | GitHub | UE5 | Real-time webcam 52-ARKit facial tracking into UE5 over LiveLink | [GitHub](https://github.com/althropic/unreal-motion) |

---

## 11. Platformer, Side-Scroller, Metroidvania & 2D / 2.5D

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **AP_Template (Action Platformer)** | GitHub | UE4/5 · MIT | Pure-Blueprint Swiss-army knife: grapple swing/pull, wall/rope/ledge/ladder/zipline climbing, portals, swimming + raft, endless runner, character switch | [GitHub](https://github.com/coquigames/AP_Template) |
| **TP_2DSideScrollerBP** | GitHub | UE5 · CC0 | Clean 2D side-scroller Blueprint template | [GitHub](https://github.com/CobraCodeDev/TP_2DSideScrollerBP) |
| **ModernSidescrollerTemplate** | GitHub | UE5–5.4 · BP | Updated 3D/2.5D side-scroller starter | [GitHub](https://github.com/matheuslaidler/ModernSidescrollerTemplate) |
| **UE5_2DPlatformer** | GitHub | UE5 · MIT | 2D platformer template | [GitHub](https://github.com/O-Y-G/UE5_2DPlatformer) |
| **PixelAdventure2D-UE5** | GitHub | UE5 · BP | Open-source 2D pixel-art Blueprint template | [GitHub](https://github.com/YspCoder/PixelAdventure2D-UE5) |
| **Captain 2D Platformer** | GitHub | UE5 · PaperZD | 2D platformer built with PaperZD + Blueprints | [GitHub](https://github.com/hnqca/captain2D-platformer-UE5) |
| **SideScrollerBP** | GitHub | UE5 · MIT | Blueprint side-scroller template | [GitHub](https://github.com/dlarkinc/SideScrollerBP) |
| **2D Hack & Slash Template** | GitHub | UE5 · BP | 2D side-scrolling combat template | [GitHub](https://github.com/Well-known-Game-Studio/2DHackSlash) |
| **UE5 Soul Boy** | GitHub | UE5 | 2.5D Souls-like dark fantasy sidescroller | [GitHub](https://github.com/3sannasia/UE5-Soul-Boy) |
| **UE4 Classic Templates for UE5** | GitHub | UE5 | Classic UE4 SideScroller2D, TwinStick, Flying & Rolling templates ported to UE5 | [GitHub](https://github.com/ScaerieTale/Unreal-Engine-4.27.2-Templates) |

---

## 12. RTS, Turn-Based Strategy, Tower Defense & City/Farm Builders

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **Skald Turn-Based Strategy** | GitHub | UE5 · C++/BP | Full turn-based strategy codebase (4,200+ commits) | [GitHub](https://github.com/Matrocoles/Skald_TurnBasedStrategy_Code) |
| **TurnBasedTacticalCombat** | GitHub | UE5 | Grid tactical turn-based combat | [GitHub](https://github.com/justAbhi77/TurnBasedTacticalCombat) |
| **UnrealRTS** | GitHub | UE5 | RTS & tower defense foundation | [GitHub](https://github.com/gcclua/UnrealRTS) |
| **ue4-rts** | GitHub | UE4/5 · MIT | Real-time strategy plugin + showcase | [GitHub](https://github.com/npruehs/ue4-rts) |
| **tower-defense-ue5** | GitHub | UE5 | Tower defense starter project | [GitHub](https://github.com/WilkinGames/tower-defense-ue5) |
| **Hive Mind** | GitHub | UE5 | Hexagon-tile turn-based strategy & building | [GitHub](https://github.com/chFleschutz/hive-mind) |
| **FarmSimulator** | GitHub | UE5 | Farming & management building template | [GitHub](https://github.com/GP2P/FarmSimulator) |
| **city-form** | GitHub | UE · MIT | Open-source city-building project | [GitHub](https://github.com/JonathanWMorris/city-form) |
| **VaFogOfWar** | GitHub | UE · Plugin | Fog of War system for RTS/MOBA | [GitHub](https://github.com/ufna/VaFogOfWar) |

---

## 13. Racing, Vehicles, 6DOF Space Flight & Drone Simulators

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **UE5 Vehicle Template** | GitHub | UE5 · BP | Modular driving mechanics + visual car damage | [GitHub](https://github.com/AnastasisMarinos/UE5-Vehicle-Template) |
| **KartingGame** | GitHub | UE5 · C++ | Multiplayer kart racing, vehicle physics & track tooling | [GitHub](https://github.com/HawkDev15/KartingGame) |
| **UE5 Steam Multiplayer Racing** | GitHub | UE 5.6 | Steam listen-server racing: lobby travel, countdown, win/loss | [GitHub](https://github.com/zawadAli/UE5-Steam-Multiplayer-Racing) |
| **RacingGame** | GitHub | UE5 | 3D racing: checkpoints, lap counter, custom tracks | [GitHub](https://github.com/prashannaantony/RacingGame) |
| **DriftScape** | GitHub | UE5 | Drift racing starter project | [GitHub](https://github.com/reyhan0173/DriftScape) |
| **DroneSimulator SDK** | GitHub | UE5 · GPL-3.0 | High-frequency multirotor physics (BEMT + arcade), PID controller, modular frames/motors/props/batteries, EdgeTX/DJI RC input | [GitHub](https://github.com/Evols/DroneSimulator) |
| **Unreal Space Program (JSBSim)** | GitHub | UE5 | Aerospace & flight physics simulator using JSBSim | [GitHub](https://github.com/finger563/unreal-space-program) |
| **FlightForge** | GitHub | UE · BSD-3 | Open-source quadcopter/drone flight simulator | [GitHub](https://github.com/ctu-mrs/flight_forge) |
| **Simple 6DOF Spaceship Example** | GitHub | UE4/5 · MIT | 6DOF zero-G spaceship Blueprints, HUD & space map | [GitHub](https://github.com/jawadato/simple-6DOF-component-example) |
| **UnrealEngineFlightProject** | GitHub | UE5 | Aircraft flight controller project | [GitHub](https://github.com/Michael-Yuan-Trebble/UnrealEngineFlightProject) |
| **PsRealVehicle** | GitHub | UE · Plugin | Force-driven vehicle simulation plugin | [GitHub](https://github.com/PushkinStudio/PsRealVehicle) |

---

## 14. Card Games, Board Games & Puzzles

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **K_Cards Game Feature** | GitHub | UE5 · C++/BP | Turn-based card game framework using GAS, AI & custom attributes | [GitHub](https://github.com/Kodingroo/K_Cards-Game-Feature) |
| **ue5-cardgame** | GitHub | UE5 · MIT | Card game plugin for UE5 | [GitHub](https://github.com/perfect-hand/ue5-cardgame) |
| **ACGCard** | GitHub | UE4/5 | Hearthstone-style CCG sample | [GitHub](https://github.com/egojump/ACGCard) |
| **UE5 Chess** | GitHub | UE5 | Full 3D chess board & ruleset | [GitHub](https://github.com/fedeg202/Chess) |
| **CryptRaider** | GitHub | UE5 | 3D first-person environmental puzzle prototype | [GitHub](https://github.com/denyskryvytskyi/CryptRaider) |
| **Unreal Simon Game** | GitHub | UE 5.4 · C++ | 2D music/memory puzzle prototype | [GitHub](https://github.com/reuttaldev/Unreal-Simon-Game) |

---

## 15. Multiplayer, Party, Co-op, Online Services (OSSv2/Steam/PlayFab) & MMO Backends

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **OnlineServicesSteam (OSSv2)** | GitHub | UE5 | Steam backend for UE5's Online Services (OSSv2) + Steam Datagram Relay net driver (works in PIE) | [GitHub](https://github.com/PoFigGames/OnlineServicesSteam) |
| **AdvancedSessionsPlugin** | GitHub | UE4/5 · MIT | Blueprint-exposed Steam/EOS/LAN sessions, lobbies, friends & voice | [GitHub](https://github.com/mordentral/AdvancedSessionsPlugin) |
| **EnhancedOnlineSessions** | GitHub | UE5 · MIT | Modern UE5 online session management plugin | [GitHub](https://github.com/MajorTomAW/EnhancedOnlineSessions) |
| **PlayFabMultiplayerUnreal** | GitHub | UE5 · MIT | Official PlayFab Online Subsystem plugin (lobbies, matchmaking, party) | [GitHub](https://github.com/PlayFab/PlayFabMultiplayerUnreal) |
| **Multiplayer Party Game Template** | GitHub | UE5 · C++ | Lobbies, modular minigames, abilities | [GitHub](https://github.com/rdelian/Multiplayer-Party-Game-Template-UE5) |
| **Bomber** | GitHub | UE5 · MIT | Clean modern UE5 multiplayer codebase | [GitHub](https://github.com/JanSeliv/Bomber) |
| **UE5 Online Multiplayer Adventure** | GitHub | UE5 · C++ | 2-player Steam co-op with GameInstance subsystem & RPCs | [GitHub](https://github.com/nbertoa/ue5-online-multiplayer-adventure) |
| **Make-Live Multiplayer** | GitHub | UE5 | Pixel Streaming multiplayer + GAS + World Partition | [GitHub](https://github.com/make-live/multiplayer) |
| **Horizon UE5 Template** | GitHub | UE5 | Dedicated game server starter template | [GitHub](https://github.com/Far-Beyond-Dev/Horizon_UE5_Template) |
| **Open World Server (OWS)** | GitHub | UE5 · MMO | Dedicated multi-zone MMO instance server backend | [GitHub](https://github.com/Dartanlla/OWS) |
| **VaRest / unreal-fetch** | GitHub | UE4/5 · MIT | Blueprint & C++ REST/JSON HTTP clients | [VaRest](https://github.com/ufna/VaRest) · [unreal-fetch](https://github.com/GameDev4K/unreal-fetch) |
| **Packt UE5 Multiplayer Samples** | GitHub | UE5 | Complete multiplayer book sample projects | [GitHub](https://github.com/PacktPublishing/Multiplayer-Game-Development-with-Unreal-Engine-5) |

---

## 16. VR / XR / AR

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **VRExpansionPlugin** | GitHub | UE4/5 · MIT | Industry-standard open-source VR framework (gripping, physics hands, climbing, sliders/levers, replication) | [GitHub](https://github.com/mordentral/VRExpansionPlugin) |
| **UE-VRHands-Template** | GitHub | UE5 · BP | Dynamic VR hands, touchscreens, grabbables & locomotion | [GitHub](https://github.com/DanielRBowen/UE-VRHands-Template) |
| **VR Multiplayer Racing** | GitHub | UE5 | Multiplayer VR racing with custom locomotion | [GitHub](https://github.com/SemyanovVisuals/race-multiplayer) |

---

## 17. Portals, Physics Sandboxes, Chaos Destruction & Level Builders

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **Wormhole Portal** | GitHub | **UE 5.8** · C++/BP | Volumetric lensing wormhole portal plugin with bidirectional actor/projectile transit, portal-aware line traces, audio/light transmission & Portal Gun demo | [GitHub](https://github.com/TeamBeaverStudio/WormholePortal) |
| **Modular Mechanics Toolkit** | GitHub | UE 5.7 · MIT | Grid-free snapping building, tactile inertia physics grabber, Chaos destruction (`BPC_BuildThrowC4`), persistent world save/load | [GitHub](https://github.com/REPIRK/Modular-Mechanics-Toolkit-UE5) |
| **UE-Grapple-Game** | GitHub | UE5 · C++ | First-person grappling hook, physics whipping, wall climbing & turrets | [GitHub](https://github.com/juaxix/UE-Grapple-Game) |
| **WorldMason** | GitHub | UE5 · MIT | Spline, instanced mesh & dynamic mesh level-building Blueprint toolkit (walls, curved stairs, rooms, bridges, domes) | [GitHub](https://github.com/StudioSyndiCatCaius/WorldMason) |
| **RealtimeMeshComponent** | GitHub | UE5 · MIT | High-performance runtime procedural mesh renderer (replaces `ProceduralMeshComponent`) | [GitHub](https://github.com/TriAxis-Games/RealtimeMeshComponent) |
| **ProceduralDungeon** | GitHub | UE4/5 | Room-based procedural dungeon generator plugin | [GitHub](https://github.com/BenPyton/ProceduralDungeon) |

---

## 18. AI, StateTree, 3D Navigation & Mass Entity Crowds

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **Gunfire3DNavigation** | GitHub | UE5 | Gunfire Games (*Remnant II*) open-source voxelized 3D navigation plugin for flying/vertical AI | [GitHub](https://github.com/GunfireGames/Gunfire3DNavigation) |
| **Nav3D** | GitHub | UE 5.6 | Sparse Voxel Octree 3D pathfinding with tactical reasoning | [GitHub](https://github.com/darbycostello/Nav3D) |
| **SDF_Grid_Navigation** | GitHub | UE5 | 6DOF volumetric Signed Distance Field + weighted A* navigation for flying, swimming & zero-G AI | [GitHub](https://github.com/Ribin545/SDF_Grid_Navigation) |
| **DLL Mass Units** | GitHub | UE5 · Apache-2.0 | Production Mass Entity crowd framework: movement, behavior LOD, engagement, scalable rendering & optional GAS | [GitHub](https://github.com/DigiLogicLabs/dll-mass-units) |
| **MassSample** | GitHub | UE5 · MIT | Community UE5 Mass Entity ECS showcase (1.1k+★) | [GitHub](https://github.com/Megafunk/MassSample) |
| **CTRL.StateTree** | GitHub | UE5 · MIT | Production StateTree tasks, utilities & property functions | [GitHub](https://github.com/ntystudio/CTRL.StateTree) |
| **Reasonable Planning AI** | GitHub | UE4/5 · MIT | Designer-driven Utility AI + GOAP extension for `AIModule` | [GitHub](https://github.com/hollsteinm/ReasonablePlanningAI) |
| **ParallelBehaviorUnreal** | GitHub | UE5 · C++ | Run multiple independent Behavior Trees in parallel on one AI pawn (combat + locomotion + dialogue) | [GitHub](https://github.com/ArtemIyX/ParallelBehaviorUnreal) |
| **Modular AI Framework / Combat EQS AI** | Fab | UE5 · BP | Blueprint data-driven enemy & EQS combat AI starters | [Modular AI](https://www.fab.com/listings/68dd9da0-80d0-4686-a8d6-92e0a3b5badd?lang=en) · [Combat EQS](https://www.fab.com/listings/517b6789-19bf-47db-9f55-facfa417559f?lang=en) |

---

## 19. World, PCG (UE 5.8), Weather, GPU Water, Foliage & 3D Gaussian Splatting

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **EssentialUE5PCG** | GitHub | **UE 5.8** · MIT | Procedural Content Generation examples & graphs for UE 5.8 | [GitHub](https://github.com/lostcrowdev/EssentialUE5PCG) |
| **FluidForge** | GitHub | UE5 · MIT | GPU-accelerated real-time water simulation plugin | [GitHub](https://github.com/AlfonsoPrograms/FluidForge) |
| **OceanResearch** | GitHub | UE5 | Gerstner wave ocean, multi-point buoyancy, dynamic weather & Niagara spray | [GitHub](https://github.com/N3onNarwhal/OceanResearch) |
| **SimpleDayNightPlugin** | GitHub | UE5 | Latitude-accurate sun/moon cycle, seasons & constellation star sphere | [GitHub](https://github.com/DKesserich/SimpleDayNightPlugin) |
| **FoliageShadowImposters** | GitHub | UE5 | Adds shadow imposters to Nanite Foliage for higher FPS | [GitHub](https://github.com/SabreDartStudios/FoliageShadowImposters) |
| **VoxelPlugin** | GitHub | UE4/5 | Real-time procedural & destructible voxel worlds | [GitHub](https://github.com/Phyronnaz/VoxelPlugin) |
| **OpenLand** | GitHub | UE4/5 | Open-source landscape auto-material | [GitHub](https://github.com/GameDev4K/unreal-open-land) |
| **MLSLabs 3D Gaussian Splatting (3DGS / 4DGS)** | GitHub | UE5 | High-performance real-time 3DGS & dynamic 4D volumetric video renderer with Sequencer playback | [GitHub](https://github.com/mlslabs/MLSLabsGaussianSplattingRenderer-UE) |

---

## 20. Stylized / Anime Toon Rendering & Audio / MetaSounds DSP

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **MooaToon** | GitHub | UE5 | Studio-grade cinematic anime/cel-shading renderer (custom shading model, hair/skin/rim/outline controls) | [GitHub](https://github.com/JasonMa0012/MooaToon) |
| **UE_CelLit** | GitHub | UE5 · MIT | Plug-in toon/cel shader for vanilla UE5 | [GitHub](https://github.com/shjh3117/UE_CelLit) |
| **UE5-StylizedPostProcess** | GitHub | UE5 | Stylized anime/painterly post-process pass | [GitHub](https://github.com/ymt3d/UE5-StylizedPostProcess) |
| **DLL Audio** | GitHub | UE5 · Apache-2.0 | Gameplay-tag driven audio events, sound definitions & listener-local budgets | [GitHub](https://github.com/DigiLogicLabs/dll-audio) |
| **Metagrain** | GitHub | UE5 · MIT | Granular synthesis nodes for UE5 MetaSounds | [GitHub](https://github.com/MaksymKokoiev/Metagrain) |
| **conv-reverb-plugin-ue5** | GitHub | UE5 | Real-time FFT overlap-add convolution reverb exposed as a native MetaSounds node | [GitHub](https://github.com/Raffiesaurus/conv-reverb-plugin-ue5) |
| **MetaSoundsSynthRepo** | GitHub | UE5 · MIT | Collection of open-source MetaSounds synthesizers | [GitHub](https://github.com/msp/MetaSoundsSynthRepo) |
| **RuntimeAudioImporter** *(UE5 fork)* | GitHub | UE5 · MIT | Load `.wav`/`.mp3`/`.ogg`/`.flac` at runtime | [Original (Archived)](https://github.com/gtreshchev/RuntimeAudioImporter) · [UE5 Fork](https://github.com/burhanaftab1/RuntimeAudioImporter) |

---

## 21. UI, Settings Menus, Loading Screens, Pooling, Validation, Telemetry & Testing

| Name | Source | UE / License | Highlights | Link |
|---|---|---|---|---|
| **Ultimate CommonUI Menu System** | GitHub | UE5 | Modular CommonUI options menu (DLSS/FSR/XeSS/TSR, Lumen, PostProcess, scalability) | [GitHub](https://github.com/Adriwin06/Ultimate-CommonUI-Menu-System) |
| **SettingsWidgetConstructor** | GitHub | UE 5.7+ | Auto-generates settings UI widgets from a DataTable | [GitHub](https://github.com/JanSeliv/SettingsWidgetConstructor) |
| **AsyncLoadingScreen / CommonLoadingScreen** | GitHub | UE5 | Non-blocking movie/widget loading screens between level loads | [AsyncLoadingScreen](https://github.com/truong-bui/AsyncLoadingScreen) · [CommonLoadingScreen](https://github.com/BastienVdW/CommonLoadingScreen) |
| **UE-BUITween** | GitHub | UE4/5 · CC0 | Lightweight C++/BP UMG UI tweening & easing library (320★) | [GitHub](https://github.com/benui-dev/UE-BUITween) |
| **UE5_PerspectiveMinimap** | GitHub | UE5 | 3D perspective minimap widget plugin | [GitHub](https://github.com/kjinwoo12/UE5_PerspectiveMinimap) |
| **Unreal5-ImGui / VesCodes ImGui** | GitHub | UE 5.4+ · MIT | Dear ImGui in-game debug menus & live telemetry inspectors | [Unreal5-ImGui](https://github.com/SLSNe/Unreal5-ImGui) · [VesCodes/imgui](https://github.com/VesCodes/imgui) |
| **PoolManager / UnrealObjectPooler** | GitHub | UE 5.7+ · MIT | World-subsystem actor/object pooling (bullets, enemies, VFX) | [PoolManager](https://github.com/JanSeliv/PoolManager) · [UnrealObjectPooler](https://github.com/FadeOutcast/UnrealObjectPooler) |
| **GameplayCameraToolset / Advanced-Camera-Manager** | GitHub | UE5 · MIT | Modular gameplay camera rigs & camera manager components | [GameplayCameraToolset](https://github.com/iEclisse/GameplayCameraToolset) · [Advanced-Camera-Manager](https://github.com/oivio/Advanced-Camera-Manager) |
| **SPUD / SaveExtension** | GitHub | UE4/5 · MIT / Apache-2.0 | Persistent streaming-world & async slot save/load frameworks | [SPUD](https://github.com/sinbad/SPUD) · [SaveExtension](https://github.com/PipeRift/SaveExtension) |
| **DataConfig** | GitHub | UE4/5 · MIT | JSON & MsgPack serialization over Unreal's Property System (241★) | [GitHub](https://github.com/slowburn-dev/DataConfig) |
| **Netflix UnrealValidationFramework** | GitHub | UE5 · Apache-2.0 | Studio-grade automated asset validation framework | [GitHub](https://github.com/Netflix-Skunkworks/UnrealValidationFramework) |
| **UE5-AssetValidator-Plugin** | GitHub | UE 5.6 · C++ | Data-driven asset validation & auto-fix editor plugin | [GitHub](https://github.com/jingchengzhao-TA/UE5-AssetValidator-Plugin) |
| **Sentry Unreal SDK** | GitHub | UE5 · MIT | Production crash reporting & error telemetry SDK | [GitHub](https://github.com/getsentry/sentry-unreal) |
| **mod.io UE Plugin** | GitHub | UE5 | In-game UGC/mod browser, download & mount pipeline | [GitHub](https://github.com/modio/modio-ue) |
| **EnhancedUnrealSpecs** | GitHub | UE5 · MIT | BDD/unit test macros on top of Unreal's Automation & `CQTest` | [GitHub](https://github.com/OpenPF2/EnhancedUnrealSpecs) |

---

## 22. Commercial / Pro Fab Frameworks (Reference)
*(Paid on Fab — listed separately from the free & open-source tools above)*

| Name | Genre | Link |
|---|---|---|
| **Ascent Combat Framework Ultimate (ACF U) V4.5** | Complete C++ Action RPG / Souls-like creator | [Fab](https://www.fab.com/listings/cc258205-8fcf-41e5-9b48-6ec44e46d7eb?lang=en) |
| **Hyper Multiplayer Survival Template Pro (MST) V4** | Full multiplayer survival, crafting & building | [Fab](https://www.fab.com/listings/6c97ce58-7cb5-4047-92f9-b060a860896d?lang=en) |
| **FPS Multiplayer Template 6** | Networked multiplayer FPS kit | [Fab](https://www.fab.com/listings/29219f54-56aa-45bb-92f9-01ca45833fe5?lang=en) |
| **Voyager: Third Person Shooter v3** | Cover, traversal, key doors, flashlight & inspection | [Fab](https://www.fab.com/listings/b3e6e357-0fff-4dec-9903-2d87a8f62b9a?lang=en) |
| **Easy TopDown Template V2.1** | Top-down survival action shooter / RPG | [Fab](https://www.fab.com/listings/5aa9fbdd-05ea-465c-911c-e6c9d2362edd?lang=en) |
| **Defender: Top-Down Shooter v3.3** | Top-down / twin-stick shooter | [Fab](https://www.fab.com/listings/502b6728-3e1c-4307-9996-2b97be4fe2e3) |
| **jRPG Template** | Turn-based JRPG party, battle & menu framework | [Fab](https://www.fab.com/listings/dc86686f-02fb-4ed0-a776-9b317c5848b0?lang=en) |

---

## 23. Giant Indexes, Blueprint Paste-Bins & Free Hubs

| Hub | What to Use It For | Link |
|---|---|---|
| **Fab — Unreal Engine** | Largest official catalog (filter **Price → Free**, **Blueprints**, **Tutorials & Examples**) | [fab.com/channels/unreal-engine](https://www.fab.com/channels/unreal-engine) · [Tutorials & Examples](https://www.fab.com/category/tutorials-examples) |
| **blueprintUE** | Thousands of copy-pasteable Blueprint node graphs (supports UE 5.8) | [blueprintue.com/type/blueprint](https://blueprintue.com/type/blueprint) |
| **itch.io Free UE Templates** | Indie Blueprint starters, PSX, horror & FPS kits | [itch.io Free UE Templates](https://itch.io/game-assets/free/tag-template/tag-unreal-engine) |
| **insthync/awesome-unreal** | 1.6k+★ categorized index of open-source UE4/UE5 repos | [GitHub](https://github.com/insthync/awesome-unreal) |
| **aiekick/Awesome_Unreal_Engine_4_-_5** | Shaders, procedural geometry, physics & tools mega-list | [GitHub](https://github.com/aiekick/Awesome_Unreal_Engine_4_-_5) |
| **SeeleAI/awesome-unreal-open-source-games** | Playable open-source Unreal projects sorted by genre | [GitHub](https://github.com/SeeleAI/awesome-unreal-open-source-games) |
| **SeeleAI/awesome-unreal-ai-tools** | Unreal MCP servers, AI agents & Blueprint automation | [GitHub](https://github.com/SeeleAI/awesome-unreal-ai-tools) |

---

## 24. Recommended Commercial-Safe Open-Source Stack (MIT / Apache-2.0)

If you want a drop-in, closed-source-safe UE 5.8 production stack:
- **Core / GAS / UI:** `AyaDogGames/GameplayFramework` (Apache-2.0) or `OmegaGameFramework` (MIT) + `XistCommonGameSample` (`CommonGame` / `GameplayMessageRouter`)
- **Locomotion + Hair/Cloth:** `ALS-Refactored` or `GASP-ALS-R` (MIT) + `KawaiiPhysics` (MIT)
- **Modular Runtime Assets:** `glTFRuntime` (MIT) + native UE 5.8 **Mutable**
- **Inventory & Equipment:** `InventoryPluginUE5` (MIT)
- **Quests & Narrative:** `FlowGraph` (MIT) + `SUQS` (MIT)
- **Save & Serialization:** `SPUD` (MIT) + `DataConfig` (MIT)
- **AI, Crowds & 3D Nav:** Native StateTree + `CTRL.StateTree` (MIT) + `DLL Mass Units` (Apache-2.0) + `Gunfire3DNavigation`
- **Pooling, Audio, Validation & Crash Telemetry:** `PoolManager` (MIT) + `DLL Audio` (Apache-2.0) + `Netflix UnrealValidationFramework` (Apache-2.0) + `sentry-unreal` (MIT)
