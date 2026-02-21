# Transition Plan: Philosophers to Soccer Players

## 📊 **Recommended Database Sources (Maximum 2)**

### 1. **Wikipedia** (Primary Source)
- **Why**: Comprehensive player biographies, career stats, playing styles, famous quotes
- **Coverage**: All legendary players have detailed Wikipedia pages
- **Extraction**: Already implemented in the codebase (`extract_wikipedia()`)
- **Data Quality**: Well-structured, multilingual, reliable

### 2. **Transfermarkt** (Secondary Source - Alternative)
- **Why**: Rich soccer-specific data (career stats, achievements, playing style, market value)
- **Coverage**: Extensive database of historical and current players
- **Format**: Structured HTML with detailed player profiles
- **Alternative**: **FIFA.com** - Official FIFA player profiles with achievements and historical data

---

## 🎯 **Oversight List of Required Changes**

### **Phase 1: Data Model & Core Domain (Python Backend)**

#### 1. **Domain Models** - `philoagents-api/src/philoagents/domain/`

**File: `philosopher.py` → Rename to `player.py`**
- [ ] Rename class `PhilosopherExtract` → `PlayerExtract`
- [ ] Rename class `Philosopher` → `SoccerPlayer`
- [ ] Update field descriptions to soccer context
- [ ] Keep structure: `id`, `name`, `perspective` (→ `playing_philosophy`), `style` (→ `playing_style`)

**File: `philosopher_factory.py` → Rename to `player_factory.py`**
- [ ] Replace `PHILOSOPHER_NAMES` dict with `PLAYER_NAMES` (10 players)
  ```python
  # Example:
  "maradona": "Diego Maradona"
  "cruyff": "Johan Cruyff"
  "pele": "Pelé"
  "ronaldo": "Ronaldo Nazário"
  "platini": "Michel Platini"
  "zidane": "Zinedine Zidane"
  "beckenbauer": "Franz Beckenbauer"
  "di_stefano": "Alfredo Di Stéfano"
  "puskas": "Ferenc Puskás"
  "garrincha": "Garrincha"
  ```

- [ ] Replace `PHILOSOPHER_PERSPECTIVES` with `PLAYER_PHILOSOPHIES` (10 entries)
  ```python
  # Example for Maradona:
  "maradona": "A creative genius who saw football as art, believing in individual
  brilliance combined with tactical awareness. He advocated for passion over systems,
  and viewed the game through the lens of street football creativity."
  ```

- [ ] Replace `PHILOSOPHER_STYLES` with `PLAYER_CONVERSATION_STYLES` (10 entries)
  ```python
  # Example for Maradona:
  "maradona": "Maradona speaks with fiery passion and emotional intensity. He's
  charismatic, sometimes provocative, and deeply connected to the working class.
  His style is direct, poetic about the game, and unapologetically confident."
  ```

- [ ] Rename class `PhilosopherFactory` → `PlayerFactory`
- [ ] Update exception names: `PhilosopherNameNotFound` → `PlayerNameNotFound`

**File: `exceptions.py`**
- [ ] Rename all exceptions:
  - `PhilosopherNameNotFound` → `PlayerNameNotFound`
  - `PhilosopherPerspectiveNotFound` → `PlayerPhilosophyNotFound`
  - `PhilosopherStyleNotFound` → `PlayerStyleNotFound`
  - `PhilosopherContextNotFound` → `PlayerContextNotFound`

**File: `prompts.py`**
- [ ] Rename `PHILOSOPHER_CHARACTER_CARD` → `PLAYER_CHARACTER_CARD`
- [ ] Update prompt template:
  ```python
  PLAYER_CHARACTER_CARD = """
  Let's roleplay. You're {{player_name}} - a legendary footballer from history...

  Player name: {{player_name}}
  Playing philosophy: {{player_philosophy}}
  Communication style: {{player_style}}

  You'll discuss football tactics, your career experiences, memorable matches,
  and your views on the beautiful game. Draw from your historical context: {{summary}}

  Retrieved memories from your career: {{player_context}}
  """
  ```

---

### **Phase 2: Data & Configuration Files**

**File: `data/extraction_metadata.json`**
- [ ] Replace 10 philosopher entries with 10 soccer players:
  ```json
  [
    {
      "id": "maradona",
      "urls": [
        "https://en.wikipedia.org/wiki/Diego_Maradona",
        "https://www.transfermarkt.com/diego-maradona/profil/spieler/73"
      ]
    },
    {
      "id": "cruyff",
      "urls": [
        "https://en.wikipedia.org/wiki/Johan_Cruyff",
        "https://www.transfermarkt.com/johan-cruyff/profil/spieler/87910"
      ]
    }
    // ... 8 more players
  ]
  ```

**File: `data/evaluation_dataset.json`**
- [ ] Replace philosopher conversations with soccer-themed Q&A
  ```json
  [
    {
      "player_id": "maradona",
      "messages": [
        {
          "role": "user",
          "content": "What made your 'Hand of God' goal so controversial?"
        },
        {
          "role": "assistant",
          "content": "..."
        }
      ]
    }
  ]
  ```

**File: `config.py`**
- [ ] Update MongoDB collection names:
  ```python
  MONGO_DB_NAME = "soccerlegends"  # or keep "philoagents"
  MONGO_STATE_CHECKPOINT_COLLECTION = "player_state_checkpoints"
  MONGO_STATE_WRITES_COLLECTION = "player_state_writes"
  MONGO_LONG_TERM_MEMORY_COLLECTION = "player_long_term_memory"
  ```

---

### **Phase 3: Application Layer (Python Backend)**

**File: `application/data/extract.py`**
- [ ] Update function signature: `get_extraction_generator(players: list[PlayerExtract])`
- [ ] Update metadata tagging:
  ```python
  metadata["player_id"] = player.id
  metadata["player_name"] = player.name
  ```
- [ ] Add Transfermarkt extractor function (if using as source 2)

**File: `application/conversation_service/workflow/state.py`**
- [ ] Rename class `PhilosopherState` → `PlayerState`
- [ ] Update fields:
  ```python
  class PlayerState(MessagesState):
      player_context: str
      player_name: str
      player_philosophy: str
      player_style: str
      summary: str
      messages: list
  ```

**File: `application/conversation_service/workflow/graph.py`**
- [ ] Update node names:
  - `retrieve_philosopher_context` → `retrieve_player_context`
- [ ] Update all variable references to use `player_*` naming

**File: `application/evaluation/generate_dataset.py`**
- [ ] Update to iterate through players instead of philosophers
- [ ] Adjust prompts to generate soccer-themed conversations

---

### **Phase 4: API Layer**

**File: `infrastructure/api.py`**
- [ ] Update endpoint parameter names:
  ```python
  class ChatMessage(BaseModel):
      message: str
      player_id: str  # was philosopher_id
  ```
- [ ] Update endpoint logic:
  ```python
  player = PlayerFactory.get_player(player_id)
  # Pass: player_name, player_philosophy, player_style
  ```
- [ ] Consider keeping endpoint paths generic (`/chat`, `/ws/chat`) or rename to `/chat-player`

---

### **Phase 5: Frontend (JavaScript/Phaser.js)**

**File: `philoagents-ui/src/scenes/Game.js`**
- [ ] Rename configuration array:
  ```javascript
  const soccerPlayerConfigs = [
      { id: "maradona", name: "Maradona", defaultDirection: "right", roamRadius: 800 },
      { id: "cruyff", name: "Cruyff", defaultDirection: "front", roamRadius: 750 },
      { id: "pele", name: "Pelé", defaultDirection: "right", roamRadius: 780 },
      { id: "ronaldo", name: "Ronaldo", defaultDirection: "front", roamRadius: 720 },
      { id: "platini", name: "Platini", defaultDirection: "front", roamRadius: 690 },
      { id: "zidane", name: "Zidane", defaultDirection: "right", roamRadius: 770 },
      { id: "beckenbauer", name: "Beckenbauer", defaultDirection: "front", roamRadius: 730 },
      { id: "di_stefano", name: "Di Stéfano", defaultDirection: "front", roamRadius: 710 },
      { id: "puskas", name: "Puskás", defaultDirection: "right", roamRadius: 740 },
      { id: "garrincha", name: "Garrincha", defaultDirection: "front", roamRadius: 760 },
  ];
  ```
- [ ] Update all references from `philosopher` to `player` in variable names

**File: `philoagents-ui/src/classes/Character.js`**
- [ ] Update frame/animation key generation (no changes needed if using `config.id`)
- [ ] Update any hardcoded "philosopher" text references

**File: `philoagents-ui/src/scenes/Preloader.js`**
- [ ] Update asset loading paths if directory names change

---

### **Phase 6: Character Assets**

**Directory: `philoagents-ui/public/assets/characters/`**
- [ ] Create new directories for each player:
  - `maradona/`, `cruyff/`, `pele/`, `ronaldo/`, `platini/`, `zidane/`, `beckenbauer/`, `di_stefano/`, `puskas/`, `garrincha/`
- [ ] For each player directory, provide:
  - Sprite sheets (PNG files)
  - `atlas.json` metadata file
  - Animations: front, back, left, right walking animations
- [ ] Remove old philosopher directories (or keep for reference)

---

### **Phase 7: CLI Tools & Commands**

**File: `tools/call_agent.py`**
- [ ] Update argument name: `--philosopher-id` → `--player-id`
  ```bash
  uv run python -m tools.call_agent --player-id "maradona" --query "What was your best goal?"
  ```

**File: `Makefile`**
- [ ] Update command names and help text:
  ```makefile
  call-agent:  # Example: --player-id "maradona"
  create-long-term-memory:  # Extracts and stores player career data
  ```

---

### **Phase 8: Documentation & Metadata**

- [ ] Update `README.md` - Replace all philosopher references with soccer players
- [ ] Update project description and examples
- [ ] Update environment variable names if needed
- [ ] Update Docker Compose service names (optional)
- [ ] Update any inline code comments referencing philosophers

---

## 📋 **Complete File Checklist**

### **Files to Rename:**
1. `domain/philosopher.py` → `domain/player.py`
2. `domain/philosopher_factory.py` → `domain/player_factory.py`

### **Files to Modify (30+ files):**

**Backend (Python):**
1. ✏️ `domain/player.py` (renamed)
2. ✏️ `domain/player_factory.py` (renamed)
3. ✏️ `domain/exceptions.py`
4. ✏️ `domain/prompts.py`
5. ✏️ `config.py`
6. ✏️ `application/data/extract.py`
7. ✏️ `application/conversation_service/workflow/state.py`
8. ✏️ `application/conversation_service/workflow/graph.py`
9. ✏️ `application/evaluation/generate_dataset.py`
10. ✏️ `infrastructure/api.py`
11. ✏️ `infrastructure/db_client.py` (if has collection name strings)
12. ✏️ `tools/call_agent.py`
13. ✏️ `data/extraction_metadata.json`
14. ✏️ `data/evaluation_dataset.json`
15. ✏️ `Makefile`
16. ✏️ `README.md`

**Frontend (JavaScript):**
17. ✏️ `philoagents-ui/src/scenes/Game.js`
18. ✏️ `philoagents-ui/src/classes/Character.js`
19. ✏️ `philoagents-ui/src/scenes/Preloader.js`
20. ✏️ `philoagents-ui/src/config/constants.js` (if exists)
21. ✏️ Any other UI files with "philosopher" references

**Assets:**
22-31. 🎨 Create 10 new player sprite directories with assets

---

## 🚀 **Implementation Strategy**

**Recommended Order:**
1. **Backend Data Models** (Phase 1) - Core domain changes
2. **Configuration & Data Files** (Phase 2) - Update metadata and configs
3. **Data Extraction** - Add Transfermarkt/FIFA scraper if needed
4. **Application Layer** (Phase 3) - Update workflows and state
5. **API Layer** (Phase 4) - Update endpoints
6. **Frontend Code** (Phase 5) - Update UI logic
7. **Character Assets** (Phase 6) - Create/source player sprites
8. **CLI & Documentation** (Phase 7-8) - Final touches

**Estimated Effort:**
- Code changes: ~250-300 lines across 30+ files
- Asset creation: 10 player sprite sheets + animations
- Data extraction: Add Transfermarkt scraper (~100 lines)
- Testing: Update evaluation dataset with soccer Q&A

---

## 📝 **Notes**

- This transition maintains the same architecture and AI agent simulation engine
- Only the domain (philosophers → soccer players) changes
- The conversation system, RAG, and LangGraph workflows remain the same
- Main effort is in data preparation and asset creation
- Consider keeping some generic terms (e.g., "agent" instead of "philosopher"/"player") for code flexibility
