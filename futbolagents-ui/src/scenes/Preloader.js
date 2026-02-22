import { Scene } from 'phaser';

export class Preloader extends Scene
{
    constructor ()
    {
        super('Preloader');
    }

    preload ()
    {
        this.load.setPath('assets');

        // General assets
        this.load.image('background', 'players_start.png');
        this.load.image('logo', 'logo.png');

        // Soccer field background (game scene)
        this.load.image('soccer-field', 'soccer-field.jpg');

        // Tilemap (used only for object/spawn-point data)
        this.load.tilemapTiledJSON("map", "tilemaps/philoagents-town.json");

        // Character assets - player (user avatar)
        this.load.atlas("sophia", "characters/sophia/atlas.png", "characters/sophia/atlas.json");

        // Character assets - soccer players
        this.load.atlas("maradona", "characters/maradona/atlas.png", "characters/maradona/atlas.json");
        this.load.atlas("cruyff", "characters/cruyff/atlas.png", "characters/cruyff/atlas.json");
        this.load.atlas("pele", "characters/pele/atlas.png", "characters/pele/atlas.json");
        this.load.atlas("ronaldo", "characters/ronaldo/atlas.png", "characters/ronaldo/atlas.json");
        this.load.atlas("suarez", "characters/suarez/atlas.png", "characters/suarez/atlas.json");
        this.load.atlas("forlan", "characters/forlan/atlas.png", "characters/forlan/atlas.json");
        this.load.atlas("beckenbauer", "characters/beckenbauer/atlas.png", "characters/beckenbauer/atlas.json");
        this.load.atlas("di_stefano", "characters/di_stefano/atlas.png", "characters/di_stefano/atlas.json");
        this.load.atlas("puskas", "characters/puskas/atlas.png", "characters/puskas/atlas.json");
        this.load.atlas("garrincha", "characters/garrincha/atlas.png", "characters/garrincha/atlas.json");

    }

    create ()
    {
        this.scene.start('MainMenu');
    }
}
