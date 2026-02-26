FROM mono:latest AS build
WORKDIR /app
COPY . .
RUN msbuild botas.csproj /p:Configuration=Release

FROM mono:latest
WORKDIR /app
COPY --from=build /app/bin/Release .
CMD ["mono", "botas.exe"]