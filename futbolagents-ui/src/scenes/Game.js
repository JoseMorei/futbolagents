import { Scene } from 'phaser';
import Character from '../classes/Character';
import DialogueBox from '../classes/DialogueBox';
import DialogueManager from '../classes/DialogueManager';

export class Game extends Scene
{
    constructor ()
    {
        super('Game');
        this.controls = null;
        this.player = null;
        this.cursors = null;
        this.dialogueBox = null;
        this.spaceKey = null;
        this.activePlayer = null;
        this.dialogueManager = null;
        this.soccerPlayers = [];
        this.labelsVisible = true;
    }

    create ()
    {
        const map = this.createTilemap();
        let screenPadding = 20;
        let maxDialogueHeight = 200;

        // Soccer field background
        this.add.image(0, 0, 'soccer-field').setOrigin(0, 0).setDepth(-1);

        this.createSoccerPlayers(map);

        this.setupPlayer(map);
        const camera = this.setupCamera(map);

        this.setupControls(camera);

        this.setupDialogueSystem();

        this.dialogueBox = new DialogueBox(this);
        this.dialogueText = this.add
            .text(60, this.game.config.height - maxDialogueHeight - screenPadding + screenPadding, '', {
            font: "18px monospace",
            fill: "#ffffff",
            padding: { x: 20, y: 10 },
            wordWrap: { width: 680 },
            lineSpacing: 6,
            maxLines: 5
            })
            .setScrollFactor(0)
            .setDepth(30)
            .setVisible(false);

        this.spaceKey = this.input.keyboard.addKey('SPACE');

        // Initialize the dialogue manager
        this.dialogueManager = new DialogueManager(this);
        this.dialogueManager.initialize(this.dialogueBox);
    }

    createSoccerPlayers(map) {
        const soccerPlayerConfigs = [
            { id: "maradona", name: "Maradona", defaultDirection: "right", roamRadius: 800 },
            { id: "cruyff", name: "Cruyff", defaultDirection: "front", roamRadius: 750 },
            { id: "pele", name: "Pelé", defaultDirection: "right", roamRadius: 780 },
            { id: "ronaldo", name: "Ronaldo", defaultDirection: "front", roamRadius: 720 },
            { id: "suarez", name: "Suarez", defaultDirection: "front", roamRadius: 690 },
            { id: "forlan", name: "Forlán", defaultDirection: "right", roamRadius: 770 },
            { id: "beckenbauer", name: "Beckenbauer", defaultDirection: "front", roamRadius: 730 },
            { id: "di_stefano", name: "Di Stéfano", defaultDirection: "front", roamRadius: 710 },
            { id: "puskas", name: "Puskás", defaultDirection: "right", roamRadius: 740 },
            { id: "garrincha", name: "Garrincha", defaultDirection: "front", roamRadius: 760 },
            {
                id: "miguel",
                name: "Miguel",
                defaultDirection: "front",
                roamRadius: 300,
                defaultMessage: "Hey there! I'm Miguel, but you can call me Mr Agent. I'd love to chat, but I'm currently writing my Substack article for tomorrow. If you're curious about my work, take a look at The Neural Maze!"
            },
            {
                id: "paul",
                name: "Paul",
                defaultDirection: "front",
                roamRadius: 300,
                defaultMessage: "Hey, I'm busy teaching my cat AI with my latest course. I can't talk right now. Check out Decoding ML for more on my thoughts."
            }
        ];

        this.soccerPlayers = [];

        soccerPlayerConfigs.forEach(config => {
            const spawnPoint = map.findObject("Objects", (obj) => obj.name === config.name);

            this[config.id] = new Character(this, {
                id: config.id,
                name: config.name,
                spawnPoint: spawnPoint,
                atlas: config.id,
                defaultDirection: config.defaultDirection,
                defaultMessage: config.defaultMessage,
                roamRadius: config.roamRadius,
                moveSpeed: config.moveSpeed || 40,
                pauseChance: config.pauseChance || 0.2,
                directionChangeChance: config.directionChangeChance || 0.3,
            });

            this.soccerPlayers.push(this[config.id]);
        });

        // Make all player labels visible initially
        this.togglePlayerLabels(true);

        // Add collisions between players
        for (let i = 0; i < this.soccerPlayers.length; i++) {
            for (let j = i + 1; j < this.soccerPlayers.length; j++) {
                this.physics.add.collider(
                    this.soccerPlayers[i].sprite,
                    this.soccerPlayers[j].sprite
                );
            }
        }
    }

    checkPlayerInteraction() {
        let nearbyPlayer = null;

        for (const soccerPlayer of this.soccerPlayers) {
            if (soccerPlayer.isPlayerNearby(this.player)) {
                nearbyPlayer = soccerPlayer;
                break;
            }
        }

        if (nearbyPlayer) {
            if (Phaser.Input.Keyboard.JustDown(this.spaceKey)) {
                if (!this.dialogueBox.isVisible()) {
                    this.dialogueManager.startDialogue(nearbyPlayer);
                } else if (!this.dialogueManager.isTyping) {
                    this.dialogueManager.continueDialogue();
                }
            }

            if (this.dialogueBox.isVisible()) {
                nearbyPlayer.facePlayer(this.player);
            }
        } else if (this.dialogueBox.isVisible()) {
            this.dialogueManager.closeDialogue();
        }
    }

    createTilemap() {
        return this.make.tilemap({ key: "map" });
    }

    setupPlayer(map) {
        const spawnPoint = map.findObject("Objects", (obj) => obj.name === "Spawn Point");
        this.player = this.physics.add.sprite(spawnPoint.x, spawnPoint.y, "sophia", "sophia-front")
            .setSize(30, 40)
            .setOffset(0, 6);

        this.soccerPlayers.forEach(soccerPlayer => {
            this.physics.add.collider(this.player, soccerPlayer.sprite);
        });

        this.createPlayerAnimations();

        // Set world bounds for physics
        this.physics.world.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
        this.physics.world.setBoundsCollision(true, true, true, true);
    }

    createPlayerAnimations() {
        const anims = this.anims;
        const animConfig = [
            { key: "sophia-left-walk", prefix: "sophia-left-walk-" },
            { key: "sophia-right-walk", prefix: "sophia-right-walk-" },
            { key: "sophia-front-walk", prefix: "sophia-front-walk-" },
            { key: "sophia-back-walk", prefix: "sophia-back-walk-" }
        ];

        animConfig.forEach(config => {
            anims.create({
                key: config.key,
                frames: anims.generateFrameNames("sophia", { prefix: config.prefix, start: 0, end: 8, zeroPad: 4 }),
                frameRate: 10,
                repeat: -1,
            });
        });
    }

    setupCamera(map) {
        const camera = this.cameras.main;
        camera.startFollow(this.player);
        camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
        return camera;
    }

    setupControls(camera) {
        this.cursors = this.input.keyboard.createCursorKeys();
        this.controls = new Phaser.Cameras.Controls.FixedKeyControl({
            camera: camera,
            left: this.cursors.left,
            right: this.cursors.right,
            up: this.cursors.up,
            down: this.cursors.down,
            speed: 0.5,
        });

        this.labelsVisible = true;

        // Add ESC key for pause menu
        this.input.keyboard.on('keydown-ESC', () => {
            if (!this.dialogueBox.isVisible()) {
                this.scene.pause();
                this.scene.launch('PauseMenu');
            }
        });
    }

    setupDialogueSystem() {
        const screenPadding = 20;
        const maxDialogueHeight = 200;

        this.dialogueBox = new DialogueBox(this);
        this.dialogueText = this.add
            .text(60, this.game.config.height - maxDialogueHeight - screenPadding + screenPadding, '', {
                font: "18px monospace",
                fill: "#ffffff",
                padding: { x: 20, y: 10 },
                wordWrap: { width: 680 },
                lineSpacing: 6,
                maxLines: 5
            })
            .setScrollFactor(0)
            .setDepth(30)
            .setVisible(false);

        this.spaceKey = this.input.keyboard.addKey('SPACE');

        this.dialogueManager = new DialogueManager(this);
        this.dialogueManager.initialize(this.dialogueBox);
    }

    update(time, delta) {
        const isInDialogue = this.dialogueBox.isVisible();

        if (!isInDialogue) {
            this.updatePlayerMovement();
        }

        this.checkPlayerInteraction();

        this.soccerPlayers.forEach(soccerPlayer => {
            soccerPlayer.update(this.player, isInDialogue);
        });

        if (this.controls) {
            this.controls.update(delta);
        }
    }

    updatePlayerMovement() {
        const speed = 175;
        const prevVelocity = this.player.body.velocity.clone();
        this.player.body.setVelocity(0);

        if (this.cursors.left.isDown) {
            this.player.body.setVelocityX(-speed);
        } else if (this.cursors.right.isDown) {
            this.player.body.setVelocityX(speed);
        }

        if (this.cursors.up.isDown) {
            this.player.body.setVelocityY(-speed);
        } else if (this.cursors.down.isDown) {
            this.player.body.setVelocityY(speed);
        }

        this.player.body.velocity.normalize().scale(speed);

        const currentVelocity = this.player.body.velocity.clone();
        const isMoving = Math.abs(currentVelocity.x) > 0 || Math.abs(currentVelocity.y) > 0;

        if (this.cursors.left.isDown && isMoving) {
            this.player.anims.play("sophia-left-walk", true);
        } else if (this.cursors.right.isDown && isMoving) {
            this.player.anims.play("sophia-right-walk", true);
        } else if (this.cursors.up.isDown && isMoving) {
            this.player.anims.play("sophia-back-walk", true);
        } else if (this.cursors.down.isDown && isMoving) {
            this.player.anims.play("sophia-front-walk", true);
        } else {
            this.player.anims.stop();
            if (prevVelocity.x < 0) this.player.setTexture("sophia", "sophia-left");
            else if (prevVelocity.x > 0) this.player.setTexture("sophia", "sophia-right");
            else if (prevVelocity.y < 0) this.player.setTexture("sophia", "sophia-back");
            else if (prevVelocity.y > 0) this.player.setTexture("sophia", "sophia-front");
            else {
                // If prevVelocity is zero, maintain current direction
                // Get current texture frame name
                const currentFrame = this.player.frame.name;

                // Extract direction from current animation or texture
                let direction = "front"; // Default

                // Check if the current frame name contains direction indicators
                if (currentFrame.includes("left")) direction = "left";
                else if (currentFrame.includes("right")) direction = "right";
                else if (currentFrame.includes("back")) direction = "back";
                else if (currentFrame.includes("front")) direction = "front";

                // Set the static texture for that direction
                this.player.setTexture("sophia", `sophia-${direction}`);
            }
        }
    }

    togglePlayerLabels(visible) {
        this.soccerPlayers.forEach(soccerPlayer => {
            if (soccerPlayer.nameLabel) {
                soccerPlayer.nameLabel.setVisible(visible);
            }
        });
    }
}
