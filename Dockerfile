FROM genepattern/docker-python36:0.4

# Create a non-root user
RUN useradd -ms /bin/bash gpuser
USER gpuser
WORKDIR /home/gpuser

# Switch back to root to create the module directory
USER root
RUN mkdir /CorrelationModule && chown gpuser /CorrelationModule

# Switch back to non-root user
USER gpuser

# Copy the wrapper script into the container
COPY src/correlation_matrix.py /CorrelationModule/

# Ensure the script is executable
RUN chmod +x /CorrelationModule/correlation_matrix.py

# Set the entrypoint to the wrapper script
ENTRYPOINT ["python3", "/CorrelationModule/correlation_matrix.py"]

# Example build and run instructions:
# docker build --rm -t genepattern/correlation-matrix:<tag> .
# docker push genepattern/correlation-matrix:<tag>
# docker run --rm -it -v /path/to/data:/mnt/mydata:rw genepattern/correlation-matrix:<tag> -i /mnt/mydata/input.gct -o /mnt/mydata/output.gct
