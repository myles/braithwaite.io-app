FROM netlify/build

WORKDIR /opt/repo
COPY ./ ./

RUN ./test-tools/test-build.sh ./ 'npm run build'
