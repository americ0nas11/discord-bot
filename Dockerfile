FROM mcr.microsoft.com/dotnet/framework/sdk:4.8 AS build
WORKDIR /app
COPY . .
RUN msbuild botas.csproj /p:Configuration=Release

FROM mcr.microsoft.com/dotnet/framework/runtime:4.8
WORKDIR /app
COPY --from=build /app/bin/Release .
CMD ["botas.exe"] 
