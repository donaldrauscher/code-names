FROM continuumio/miniconda3:4.4.10

ENV PORT 8050
ENV CONDA_ENV code-names
ENV GLOVE_MODEL glove.6B.50d
ENV GUNICORN_WORKERS 3
ENV APP_DIR /app

WORKDIR $APP_DIR

RUN apt-get update \
  && apt-get install -y unzip gzip \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt app.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

RUN conda create -n ${CONDA_ENV} \
  && export PATH=/opt/conda/envs/$CONDA_ENV/bin:$PATH \
  && while read req; do pip install --no-cache-dir --upgrade $req; done < requirements.txt

RUN wget -q http://nlp.stanford.edu/data/glove.6B.zip \
  && unzip glove.6B.zip -d glove \
  && rm glove.6B.zip \
  && python -m gensim.scripts.glove2word2vec --input glove/${GLOVE_MODEL}.txt --output glove/w2v.${GLOVE_MODEL}.txt \
  && gzip glove/w2v.${GLOVE_MODEL}.txt \
  && rm glove/*.txt

EXPOSE $PORT

ENTRYPOINT $APP_DIR/entrypoint.sh