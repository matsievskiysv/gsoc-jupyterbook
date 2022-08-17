import os
from subprocess import check_call

def post_save(model, os_path, contents_manager):
    """post-save hook for converting notebooks to .py scripts"""
    if model['type'] != 'notebook':
        return # only do this for notebooks
    d, fname = os.path.split(os_path)
    if ".py" in fname:
        return # Ignore python files
    check_call(['jupyter', 'nbconvert', '--to', "html",
                "--TagRemovePreprocessor.remove_input_tags={\'remove-input\', \'hide-input\'}",
                fname, "--template", "reveal", f"--output=html/{fname.split('.ipynb')[0]}"], cwd=d)

c.FileContentsManager.post_save_hook = post_save

