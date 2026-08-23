# LangGraph Workflow

LangGraph should orchestrate the ML pipeline. SQLite stores data, the encoder turns FEN strings into tensors, and PyTorch handles model training.

## Dataset Preparation

```mermaid
flowchart TD
    START([START]) --> LoadRows[load_training_positions]
    LoadRows --> EncodeRows[encode_positions]
    EncodeRows --> ValidateExamples[validate_examples]
    ValidateExamples --> SummarizeDataset[summarize_dataset]
    SummarizeDataset --> END([END])

    LoadRows -. reads .-> SQLite[(SQLite)]
    EncodeRows -. uses .-> Encoder[Board Encoder]
    ValidateExamples -. checks .-> Rules[Shape and Target Rules]
```

## State

```text
rows
  Raw rows from SQLite.

examples
  Encoded tensor and value target pairs.

bad_rows
  Rows that failed encoding or validation.

summary
  Counts and target distribution.
```

## Later Training Extension

```mermaid
flowchart TD
    START([START]) --> LoadRows[load_training_positions]
    LoadRows --> EncodeRows[encode_positions]
    EncodeRows --> ValidateExamples[validate_examples]
    ValidateExamples --> SplitDataset[split_dataset]
    SplitDataset --> TrainValueModel[train_value_model]
    TrainValueModel --> EvaluateModel[evaluate_model]
    EvaluateModel --> SaveCandidate[save_candidate]
    SaveCandidate --> PromoteOrReject[promote_or_reject]
    PromoteOrReject --> END([END])

    LoadRows -. reads .-> SQLite[(SQLite)]
    EncodeRows -. uses .-> Encoder[Board Encoder]
    TrainValueModel -. uses .-> PyTorch[PyTorch]
    EvaluateModel -. compares .-> CurrentModel[Current Model]
```

The first graph should only prepare and validate data. Training comes after the data path is reliable.
