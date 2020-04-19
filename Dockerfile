FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

RUN apt-get update \
    && apt-get install -y --no-install-recommends tabix 

RUN mkdir -p /jbrowse/ && git clone --recursive https://github.com/gmod/jbrowse /jbrowse/ && \
    cd /jbrowse/ && \
    git checkout 1.12.3-release && ./setup.sh


WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
