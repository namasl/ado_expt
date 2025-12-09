This is a simple demo using [ado](https://github.com/ibm/ado) to decorate functions in a package.

## Set up environment

Set up a virtual environment
```bash
python -m venv ~/venv_ado
source ~/venv_ado/bin/activate
```

Install ado
```bash
git clone https://github.com/IBM/ado.git
cd ado
pip install .
pip install ado-ray-tune
```

Set up this demo
```bash
git clone https://github.com/namasl/ado_expt.git
cd ado_expt
pip install -e .
```

## Do stuff

> [!NOTE]
> Data and metadata from ado are stored in `~/.config/ado/` (Linux) or `~/Library/Application Support/ado/` (Mac).

### Check actuator

In root of `ado_expt`, ensure the `bar_details` actuator shows up (under "EXPERIMENT ID").
```bash
ado get actuators --details
```

See details about the custom experiment. This is information related to details passed to the `@custom_experiment` decorator.
```bash
ado describe experiment bar_details
```

### Execute a point experiment

Run an experiment at a single point specified in `point.yaml` and show results.
```bash
run_experiment point.yaml
```

### Make a discovery space

Set context
```bash
ado context local
```

Create the space defined in `space.yaml`. This will be a subspace of the entire searchable space defined in the `@custom_experiment` decorator.
```bash
ado create space -f space.yaml --use-default-sample-store
```
Grab the space identifier printed out with that command, it will look something like `space-26dd95-default`.

See what spaces are available
```bash
ado get space
```

Describe the space (we'll get the latest, which we just defined).
```bash
ado describe space --use-latest
```
The details here will match what is defined in `space.yaml` which we used to create this space.

### Run operation

Create an operator using the discovery space we just created. This will run a set of experiments as defined in `operation.yaml`.
```bash
ado create operation -f operation.yaml --use-latest space
```

See all operations
```bash
ado get operation
```

Results from running the operator are stored in a `datacontainer` resource. Get the ID of the `datacontainer`, which will look something like `datacontainer-ae536e7d`.
```bash
ado show related operation --use-latest
```

Get results from the `datacontainer`
```bash
ado describe datacontainer datacontainer-ae536e7d
```

To see details of all configurations tested in the operation
```bash
ado show entities operation --use-latest
```
