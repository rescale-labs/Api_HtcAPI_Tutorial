# The Rescale HTC Tutorial

[Rescale HTC](https://rescale.com/platform/hpc-as-a-service/high-throughput-computing/) is a High-Throughput Computing framework that can orchestrates millions of massively parallel jobs in minutes on hundreds of thousands of cores across multiple clouds and best-fit architectures with 99.99% job success. It can scale up large clusters in minutes to accelerate R&D exploration and scale down when idle to decrease costs.

HTC workloads are mostly fully automated. Multiple continuous integration pipelines prepare inputs, launch jobs and process results. Majority of HTC applications need to drive execution programmatically. That's why Rescale HTC is an API driven platform.

This executable tutorial walks through an end-to-end example, from workload containerization to submission, monitoring and cancellation. It is best to set up a local environment and go though it locally. See [rescale_htc_tutorial.ipynb](rescale_htc_tutorial.ipynb) for the code preview.

## Environment setup

The tutorial assumes a Unix OS (for Windows, see [The Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install)). If running this tutorial in a Windows command prompt is desired - then all code cells staring with `! command` need to be ported to Windows commands.

To enable container image creation and local testing, a [Docker](https://www.docker.com/products/docker-desktop/) runtime needs to be installed.

Direct interaction with AWS S3 storage requires the [AWS CLI](https://aws.amazon.com/cli/).

Version 3.6+ of a Python interpreter is required.

To launch the notebook, clone the repository (or unzip the downloaded tutorial archive). Change your working directory to the directory containing the `rescale_htc_api_tutorial.ipynb` file. Run the following to set up the virtual environment, fetch dependencies and launch the notebook.

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt -U \
    --extra-index-url http://rescale-htc-cli-agae5ucedee8kohtaet8naekx.s3-website-eu-west-1.amazonaws.com \
    --trusted-host rescale-htc-cli-agae5ucedee8kohtaet8naekx.s3-website-eu-west-1.amazonaws.com
$ jupyter notebook rescale_htc_tutorial.ipynb
```

![](README.assets/htc_tutorial_notebook.gif)

## About the author and Rescale

[Rescale™](https://rescale.com) is a technology company that builds cloud software and services that enable organizations of every size to deliver engineering and scientific breakthroughs that enrich humanity.

[Bartek Dobrzelecki](https://linkedin.com/in/bardobrze) is a Senior Customer Success Engineer at Rescale with a background in High Performance Computing and Software Engineering. He is always keen to share his knowledge, demystify technology and democratize computational thinking. He strongly believes that no technology should be indistinguishable from magic.