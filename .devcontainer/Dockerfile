# Use miniconda as base image
FROM continuumio/miniconda3:latest

# Copy environment yml and test requirements first (as root)
COPY ci/environment-docs.yml /tmp/environment-docs.yml

# Create conda environment from ci/environment-docs.yml (as root)
RUN conda env update -n base -f /tmp/environment-docs.yml && \
    conda clean --all --yes

# Create a non-root user
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y --no-install-recommends sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to the non-root user
USER $USERNAME

# Set working directory
WORKDIR /home/$USERNAME/workspace

# Set environment variables
ENV PATH="/home/$USERNAME/.local/bin:/opt/conda/bin:${PATH}" \
    PYTHONUNBUFFERED=1

# Install the package in development mode
# NOTE: This is commented out to speed up the build process during development and there are rapid changes to the source code
# TODO: Uncomment here and remove from postCreateCommand in devcontainer.json once development slows down
# RUN pip install -e .

# Set default command
CMD ["/bin/bash"]