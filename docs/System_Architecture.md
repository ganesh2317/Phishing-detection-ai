# System Architecture

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    User[User / Client] -->|HTTP Request| Frontend[Frontend UI (Glassmorphism)]
    Frontend -->|REST API| Backend[Backend API (FastAPI)]
    
    subgraph "Backend Services"
        Backend -->|Predict| ModelEngine[AI Model Engine]
        Backend -->|Chat| Chatbot[Chatbot Service]
        Backend -->|Log| Database[(Database / Logs)]
    end
    
    subgraph "AI Core"
        ModelEngine -->|Text| TFIDF[TF-IDF Vectorizer]
        ModelEngine -->|URL| FeatureExt[Feature Extractor]
        TFIDF --> MLModel[ML Model (Random Forest)]
        FeatureExt --> URLModel[URL Model]
        MLModel -->|Result| Backend
        URLModel -->|Result| Backend
    end
    
    subgraph "Data Layer"
        Dataset[Datasets] --> Preprocess[Preprocessing]
        Preprocess --> Training[Model Training]
        Training --> MLModel
    end
```

## Component Description

1.  **Frontend**: The user interface where users input data. Built with basic HTML/CSS/JS for lightweight deployment.
2.  **Backend API**: The central controller built with FastAPI. It routes requests to the appropriate service.
3.  **Model Engine**: Loads the trained `.pkl` models and performs inference.
4.  **Chatbot Service**: A rule-based (expandable to LLM) agent for user interaction.
