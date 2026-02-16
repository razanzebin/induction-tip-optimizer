import json, copy, subprocess
from pathlib import Path
import optuna

REPO = Path(__file__).resolve().parents[1]
RUN_ONE = REPO / "pipeline" / "run_one.py"

def run_and_get_objective(params: dict) -> float:
    tmp = REPO / "pipeline" / "_tmp_params.json"
    tmp.write_text(json.dumps(params, indent=2))
    # run_one prints OBJ, but we will read metrics.json from newest run folder instead.
    subprocess.check_call(["python3", str(RUN_ONE), str(tmp)])

    runs_dir = REPO / "results" / "runs"
    latest = sorted(runs_dir.iterdir())[-1]
    metrics = json.loads((latest / "metrics.json").read_text())
    return float(metrics["objective"])

def main():
    base = json.loads((REPO / "pipeline" / "params_default.json").read_text())

    def objective(trial: optuna.Trial) -> float:
        p = copy.deepcopy(base)
        p["tip_length_mm"] = trial.suggest_float("tip_length_mm", 6.0, 18.0)
        p["tip_radius_mm"] = trial.suggest_float("tip_radius_mm", 1.0, 6.0)
        p["wall_thickness_mm"] = trial.suggest_float("wall_thickness_mm", 0.2, 1.5)
        # inner depth cannot exceed length
        p["inner_depth_mm"] = trial.suggest_float("inner_depth_mm", 0.0, p["tip_length_mm"])
        return run_and_get_objective(p)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20)

    out = REPO / "results" / "optuna_best.json"
    out.write_text(json.dumps({
        "best_value": study.best_value,
        "best_params": study.best_params
    }, indent=2))

    print("\nBEST:", study.best_value)
    print("PARAMS:", study.best_params)
    print("Saved:", out)

if __name__ == "__main__":
    main()
