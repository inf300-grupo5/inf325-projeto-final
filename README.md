### [Option 1] Launching this lab as a local container from a remote git repository using [repo2docker](https://github.com/jupyter/repo2docker)

1.  On a terminal, enter a folder of your preference and create a new Python virtual environment (venv):
```
python3 -m venv venv
``` 

3. Activate your virtual environment (you may do this again later if you want to restart your container):
```
source venv/bin/activate
```

4. Install/upgrade required Python libs using pip:
```
pip install jupyter-repo2docker pip -U
```

5. Launch the Docker container using `repo2docker` directly from the remote repository:

```bash
jupyter-repo2docker -p 8888:8888 https://github.com/thedatasociety/lab-neo4j \ 
                    jupyter lab --ip 0.0.0.0 --NotebookApp.token='mytoken'
```
Each interface will be available at a specific path, as follows:

* **JupyterLab**: http://127.0.0.1:8888/lab?token=mytoken

* **Jupyter**: http://127.0.0.1:8888/tree?token=mytoken

* **VSCode**:  http://127.0.0.1:8888/vscode?token=mytoken


See the [repo2docker](https://github.com/jupyter/repo2docker) documentation for more details [regarding the use of multiple interfaces](https://mybinder.readthedocs.io/en/latest/howto/user_interface.html) and other configs.    
