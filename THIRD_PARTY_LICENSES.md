# Third-Party License Inventory

Status: preliminary internal check, not legal advice.

This public release is a static artifact/evidence package. It vendors no
third-party code.

| Dependency | Scope | Runtime required | License status |
|---|---:|---:|---|
| arc-agi / arcengine | Kaggle competition-provided runtime referenced by the linked notebook | yes, in Kaggle evaluation context | not redistributed in this public release |
| pandas | Kaggle notebook output helper | yes, in Kaggle notebook context | Kaggle/runtime dependency, not vendored |
| python-dotenv | Kaggle sample-notebook setup dependency | yes, in Kaggle notebook context | Kaggle/runtime dependency, not vendored |

The package-candidate `requirements.txt` remains intentionally empty because
the public release does not redistribute runtime wheels or third-party source.
Review dependency terms separately before creating a new executable package.
