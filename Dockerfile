FROM continuumio/miniconda3:4.4.10

ENV PORT 8050
ENV CONDA_ENV code-names
ENV PATH /opt/conda/envs/$CONDA_ENV/bin:$PATH

RUN apt-get update
RUN apt-get install unzip

WORKDIR /app

COPY requirements.txt .
RUN conda create -n ${CONDA_ENV}
RUN while read req; do pip install --upgrade $req; done < requirements.txt

#RUN wget http://nlp.stanford.edu/data/glove.6B.zip
COPY glove.6B.zip .
RUN unzip glove.6B.zip -d glove && rm glove.6B.zip
RUN python -m gensim.scripts.glove2word2vec --input glove/glove.6B.50d.txt --output glove/w2v.glove.6B.50d.txt
RUN rm glove/glove.6B.*.txt

ADD app.py .
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE $PORT

ENTRYPOINT ["/bin/bash", "-c", "entrypoint.sh"]