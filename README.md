# Orbit — Astronomy Assistant

A runnable local astronomy chatbot plus a trainable PyTorch CNN for galaxy images.
The text feature is a small keyword-based reference retriever, not a generative language model.
It does not understand arbitrary questions or retain conversational context.
No API key, account, or package installation is needed for text chat.

## Run

From this folder in PowerShell:

```powershell
python app.py
```

Open http://127.0.0.1:8000. Stop with Ctrl+C.
Ask about black holes, stars, galaxies, galaxy shapes, planets, the Moon,
light-years, exoplanets, the Big Bang, dark matter, or supernovae.
Answers include reference links. No live news or observing forecasts.

## Train the CNN

No dataset or pretrained checkpoint is bundled. The interface explicitly reports
that classification is unavailable until you train a model.

Create an environment and install optional dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-cnn.txt
```

Use real, licensed, labeled galaxy photographs, arranged like this:

```text
data/
  train/
    elliptical/
    irregular/
    spiral/
  val/
    elliptical/
    irregular/
    spiral/
```

Put JPG or PNG images inside each class folder. Both splits must contain all three
classes. Aim for hundreds or more diverse examples per class. Keep all images of
the same astronomical object in the same split to avoid leakage. Hold back a
separate test set for final evaluation; do not use it to select checkpoints.
Check class balance and labels. Galaxy Zoo is a possible labeling resource, but
its original labels need a documented mapping; do not blindly rename categories.
Spiral/elliptical/irregular is a simplified taxonomy, excluding some real types.

```powershell
.\.venv\Scripts\python.exe train.py --data data --epochs 15
.\.venv\Scripts\python.exe app.py
```

Training uses three convolutional layers, augmentation, cross-entropy, Adam, and
a fixed seed. It saves the checkpoint with best validation accuracy to
models/galaxy_cnn.pt and writes epoch metrics and confusion matrices to
models/training_history.json. Confusion matrix rows are actual labels and columns
are predictions, ordered elliptical, irregular, spiral.

Refresh the page after training. Inference runs on CPU and loads only the local
checkpoint. Softmax scores are uncalibrated; unrelated images can receive high
scores. Validation accuracy is not a substitute for independent test performance.
No accuracy claim is made before training and evaluation.

## Checks

```powershell
python -B -m unittest discover -s tests -v
```

These test retrieval and API behavior without CNN dependencies.
The CNN requires a separate training and inference check with real data.

## Files

- app.py: local HTTP server and JSON endpoints.
- chatbot.py: reference topics and matching.
- index.html: responsive chat and image interface.
- cnn.py: architecture, preprocessing, inference.
- train.py: supervised training and validation.

## References

- https://science.nasa.gov/universe/galaxies/types/
- https://science.nasa.gov/universe/galaxies/
- https://pytorch.org/get-started/locally/

This is a local learning prototype; keep the server bound to localhost.
