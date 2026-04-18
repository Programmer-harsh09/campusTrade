# Graph Report - C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade  (2026-04-19)

## Corpus Check
- 24 files · ~17,442 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 152 nodes · 252 edges · 17 communities detected
- Extraction: 63% EXTRACTED · 37% INFERRED · 0% AMBIGUOUS · INFERRED: 93 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]

## God Nodes (most connected - your core abstractions)
1. `get_supabase_client()` - 19 edges
2. `AskCreate` - 10 edges
3. `AskUpdate` - 10 edges
4. `AskResponse` - 10 edges
5. `ListingCreate` - 10 edges
6. `ListingUpdate` - 10 edges
7. `ListingResponse` - 10 edges
8. `get_ask_by_id()` - 8 edges
9. `get_listing_by_id()` - 8 edges
10. `AuthTokenResponse` - 7 edges

## Surprising Connections (you probably didn't know these)
- `list_asks()` --calls--> `get_asks()`  [INFERRED]
  C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\api\routers\asks.py → C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\repositories\ask_repo.py
- `my_asks()` --calls--> `get_my_asks()`  [INFERRED]
  C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\api\routers\asks.py → C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\repositories\ask_repo.py
- `get_ask()` --calls--> `get_ask_by_id()`  [INFERRED]
  C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\api\routers\asks.py → C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\repositories\ask_repo.py
- `update_ask()` --calls--> `get_ask_by_id()`  [INFERRED]
  C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\api\routers\asks.py → C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\repositories\ask_repo.py
- `signup()` --calls--> `sign_up()`  [INFERRED]
  C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\api\routers\auth.py → C:\Users\harsh\OneDrive\Desktop\MINI Project\CampusTrade\app\services\auth_service.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (20): _assert_owner(), create_listing(), delete_listing(), get_listing_by_id(), get_listings(), get_my_listings(), Listing repository — Supabase CRUD operations for the ``listings`` table., Return all listings owned by the authenticated user. (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.17
Nodes (19): AuthTokenResponse, login(), LoginRequest, Auth schemas — request models for signup / login and token responses., Payload for new user registration., Create a new CampusTrade account.      - Any valid email is accepted (no .edu re, Payload for email/password sign-in., Tokens returned after successful login. (+11 more)

### Community 2 - "Community 2"
Cohesion: 0.19
Nodes (19): AskCreate, AskResponse, AskUpdate, Payload for creating a new ask / buy-request., Fields a requester can update on their ask., Full ask data returned by the API., create_ask(), delete_ask() (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (19): ListingCreate, ListingResponse, ListingUpdate, Payload for creating a new listing., Fields a seller can update on their listing., Full listing data returned by the API., create_listing(), delete_listing() (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (15): AskStatus, AskUrgency, Ask schemas — request and response models for buy-requests., create_ask(), Insert a new ask / buy-request for the authenticated user.      ``payload`` shou, Authentication service — wrappers around Supabase GoTrue auth.  Handles standard, Register a new user with Supabase Auth.      The handle_new_user() DB trigger au, Authenticate an existing user with email + password.      Returns:         dict (+7 more)

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (15): _assert_owner(), delete_ask(), get_ask_by_id(), get_asks(), get_my_asks(), Ask repository — Supabase CRUD operations for the ``asks`` table., Return all asks owned by the authenticated user., Update an ask only if the authenticated user is the requester.      ``updates`` (+7 more)

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (9): BaseSettings, get_settings(), Application configuration loaded from environment variables.  Uses Pydantic Base, Central settings object.      Attributes:         APP_NAME:      Display name us, Return a cached Settings instance.      Using @lru_cache ensures the .env file i, Settings, health_check(), Health-check router.  Provides liveness and readiness probes for monitoring and (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.25
Nodes (6): Media router — image upload endpoint.  Authenticated users can upload images; th, Upload an image to CampusTrade media storage.      Requires a valid Bearer token, Media service — handles image validation and upload to Supabase Storage.  Suppor, Validate and upload an image to Supabase Storage.      Args:         file: A Fas, upload_image(), upload_media()

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (3): CampusTrade API — Application Entry Point  A student marketplace backend built w, Redirect-friendly landing that confirms the API is running., root()

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (3): get_current_user_id(), Auth dependency — verifies the Supabase JWT and returns the current user ID.  Us, Validate the Bearer token via Supabase ``auth.get_user()``.      Returns:

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (0): 

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (0): 

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **51 isolated node(s):** `CampusTrade API — Application Entry Point  A student marketplace backend built w`, `Redirect-friendly landing that confirms the API is running.`, `Health-check router.  Provides liveness and readiness probes for monitoring and`, `Return basic service health information.`, `Media router — image upload endpoint.  Authenticated users can upload images; th` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_supabase_client()` connect `Community 0` to `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 9`?**
  _High betweenness centrality (0.386) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `Community 6` to `Community 0`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `upload_image()` connect `Community 7` to `Community 0`, `Community 4`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `get_supabase_client()` (e.g. with `get_current_user_id()` and `get_settings()`) actually correct?**
  _`get_supabase_client()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `str` (e.g. with `get_current_user_id()` and `create_ask()`) actually correct?**
  _`str` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `AskCreate` (e.g. with `Asks router — RESTful CRUD endpoints for buy-requests ("Ask Mode").  Public:   G` and `Post a new buy-request (ask) for the authenticated user.      Requires a valid B`) actually correct?**
  _`AskCreate` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `AskUpdate` (e.g. with `Asks router — RESTful CRUD endpoints for buy-requests ("Ask Mode").  Public:   G` and `Post a new buy-request (ask) for the authenticated user.      Requires a valid B`) actually correct?**
  _`AskUpdate` has 7 INFERRED edges - model-reasoned connections that need verification._