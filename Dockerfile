FROM netlify/build

WORKDIR /opt/repo
COPY ./ ./

RUN build npm run-script build
