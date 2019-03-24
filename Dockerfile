FROM netlify/build:xenial

WORKDIR /opt/repo
COPY ./ ./

RUN npm --version

RUN build 'npm run build'

