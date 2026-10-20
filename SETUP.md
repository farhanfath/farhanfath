# Setup

1. Back up your existing GitHub profile README.
2. Copy this package's contents into the root of `farhanfath/farhanfath` (including `.github/workflows/generate-ascii.yml`). Preserve your existing snake workflow and `output` branch.
3. Run `pip install -r requirements.txt` and `python scripts/generate_profile.py` to preview or regenerate locally.
4. Commit and push to `main`. The profile README automatically chooses light/dark SVG using `<picture>`.
5. In GitHub repository Settings → Actions → General → Workflow permissions, allow read and write permissions if the workflow's push is denied. For protected branches, generate and commit the SVGs locally or via PR instead.
6. To change the portrait, replace `assets/portrait.png` and run the generator again. The crop and contrast are configurable in `scripts/generate_profile.py`.

Existing GitHub stats and contribution snake depend on third-party endpoints / your existing snake workflow. The new ASCII workflow does not replace that workflow.

The portrait is committed publicly to the repository. If you don't want the original photo published, generate the SVGs locally, remove the photo from the repo, and adjust the workflow to avoid regenerating from a missing source.
