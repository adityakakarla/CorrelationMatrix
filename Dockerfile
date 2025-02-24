FROM genepattern/docker-python36:0.4

# Create a non-root user
RUN useradd -ms /bin/bash gpuser

# Create module directory as root
RUN mkdir /CorrelationModule

# Copy the wrapper script as root
COPY src/correlation_matrix.py /CorrelationModule/

RUN chmod 777 /CorrelationModule/correlation_matrix.py
# Switch back to non-root user

# Change ownership and permissions as root
RUN chown -R gpuser:gpuser /CorrelationModule && \
    chmod +x /CorrelationModule/correlation_matrix.py

# Now switch to non-root user
USER gpuser
WORKDIR /home/gpuser

# Set the entrypoint
ENTRYPOINT ["python3", "/CorrelationModule/correlation_matrix.py"]

# Example build and run instructions:
# docker build --rm -t genepattern/correlation-matrix:<tag> .
# docker push genepattern/correlation-matrix:<tag>
# docker run --rm -it -v /path/to/data:/mnt/mydata:rw genepattern/correlation-matrix:<tag> -i /mnt/mydata/input.gct -o /mnt/mydata/output.gct