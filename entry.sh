#!/bin/bash
set -e

echo "Checking mandatory input variables..."

declare -A mandatory_vars

mandatory_vars=( ["tla"]="${tla}" ["env"]="${env}" ["version"]="${version}")

for key in "${!mandatory_vars[@]}"
do
  if [  "${mandatory_vars[$key]}" == " " ] || [ -z "${mandatory_vars[$key]}" ]; then
      echo "'${key}' variable is empty, failing..."
      exit 1
  fi
done

declare -A optional_vars

# shellcheck disable=SC2034
optional_vars=( ['brand']="${brand}" ['appVersion']="${appVersion}" ['body']="${body}" )

echo "All variables are present. Continuing..."

echo "Getting sorted tags..."
tags=$(git tag -l --sort=v:refname)

echo "Tags: $tags"
old_tag=$( (echo "$tags" | grep "$env" | grep "$brand" || echo "$tags") | tail -n 1)
new_tag=v$version$brand-$env

echo "Old tag: $old_tag - New tag: $new_tag"
echo "Creating a new tag..."
git tag "${new_tag}"

release_name="Release $new_tag"
echo "Created new ${release_name}"

{
  echo "old_tag=$old_tag"
  echo "new_tag=$new_tag"
  echo "release_name=$release_name"
}  >> "$GITHUB_OUTPUT"

echo "Fetching commits between tags - $old_tag and $new_tag..."
EOF=$(dd if=/dev/urandom bs=15 count=1 status=none | base64)
release_message=$(git log --pretty=medium "$old_tag".."$new_tag" | tr '\n' '\n')
info_message=""

if [ -n "${appVersion}" ] || [ "${appVersion}" != " " ]; then
  info_message="This release uses a published package with version $appVersion"
fi

if [  -z "${release_message}"  ] || [ "${release_message}" == " "  ]; then
  {
    echo "release_message<<$EOF"
    if [ -n "${info_message}" ];then
      printf '\n'
      echo "$info_message"
    fi
    if [ -n "${body}" ]; then
      printf '\n'
      echo "$body"
    fi
    printf '\n'
    echo "No new changes between old tag ${old_tag} and new tag ${new_tag}."
    printf '\n'
    echo "$EOF"
  } >> "$GITHUB_OUTPUT"
else
  {
    echo "release_message<<$EOF"
    if [ -n "${info_message}" ];then
      printf '\n'
      echo "$info_message"
    fi
    if [ -n "${body}" ]; then
      printf '\n'
      echo "$body"
    fi
    printf '\n Commits \n'
    echo "$release_message"
    printf '\n'
    echo "$EOF"
  } >> "$GITHUB_OUTPUT"
fi