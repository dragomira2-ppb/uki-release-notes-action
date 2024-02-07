#!/bin/bash
set -e

echo "Checking mandatory input variables..."

declare -A mandatory_vars

mandatory_vars=( ["tla"]="${{ inputs.tla }}" ["environment"]="${{ inputs.environment }}" ["brand"]="${{ inputs.brand }}" ["version"]="${{ inputs.version }}" ["appVersion"]="${{ inputs.appVersion }}")

for key in "${!mandatory_vars[@]}"
do
  if [  "${mandatory_vars[$key]}" == " " ] || [ -z "${mandatory_vars[$key]}" ]; then
      echo "'${key}' variable is empty, failing..."
      exit 1
  fi
done

echo "All variables are present. Continuing..."

version=v${{ inputs.version }
brand=${{ inputs.brand }}
env=${{ inputs.environment }}

echo "Getting sorted tags..."
tags=$(git tag -l --sort=v:refname)

echo "Tags: $tags"
old_tag=$( (echo "$tags" | grep $env | grep $brand || echo "$tags") | tail -n 1)
new_tag=$version$brand-$env

echo "Old tag: $old_tag - New tag: $new_tag"
echo "Creating a new tag in git..."
git tag "${new_tag}"

release_name="Release $new_tag"
echo "Created new release ${release_name}"

echo "old_tag=$old_tag" >> "$GITHUB_OUTPUT"
echo "new_tag=$new_tag" >> "$GITHUB_OUTPUT"
echo "release_name=$release_name" >> "$GITHUB_OUTPUT"

echo "Fetching commits between tags - $old_tag and $new_tag..."
release_message=$(git log --pretty=medium "$old_tag".."$new_tag"| tr '\n' '\n')

if [  -z "${release_message}"  ] || [ "${release_message}" == ""  ]; then
  release_message="No new changes between old tag ${old_tag} and new tag ${new_tag}."
else
  echo "${release_message}"
fi

EOF=$(dd if=/dev/urandom bs=15 count=1 status=none | base64)
echo "release_message<<$EOF" >> "$GITHUB_OUTPUT"
echo -e "This release uses a published package with version ${{ inputs.appVersion }}.\n\n" >> "$GITHUB_OUTPUT"
echo "$release_message" >> "$GITHUB_OUTPUT"
echo "$EOF" >> "$GITHUB_OUTPUT"