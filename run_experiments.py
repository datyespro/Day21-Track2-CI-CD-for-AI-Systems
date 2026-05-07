import yaml
import subprocess
import os

os.environ["MLFLOW_TRACKING_URI"] = "sqlite:///mlflow.db"
os.environ["MLFLOW_ARTIFACT_ROOT"] = "./mlartifacts"

import random

best_acc = 0
best_params = None

for i in range(5):
    params = {
        "n_estimators": random.choice([200, 300, 500]),
        "max_depth": random.choice([None, 20, 30]),
        "min_samples_split": random.choice([2, 3]),
        "class_weight": random.choice([None, "balanced"]),
        "criterion": random.choice(["gini", "entropy"])
    }
    with open("params.yaml", "w") as f:
        yaml.dump(params, f)
    
    res = subprocess.run([".venv\\Scripts\\python.exe", "src/train.py"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in run {i}: {res.stderr}")
    out = res.stdout
    for line in out.split("\n"):
        if line.startswith("Accuracy:"):
            acc = float(line.split("|")[0].replace("Accuracy: ", "").strip())
            if acc > best_acc:
                best_acc = acc
                best_params = params
            print(f"Tested {params} -> {acc}")

print(f"Best: {best_params} with {best_acc}")
