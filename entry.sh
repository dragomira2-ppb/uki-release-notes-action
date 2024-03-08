#!/bin/bash
set -e

echo "Checking mandatory input variables..."

declare -A mandatory_vars

mandatory_vars=( ["env"]="${env}" ["version"]="${version}")

for key in "${!mandatory_vars[@]}"
do
  if [  "${mandatory_vars[$key]}" == " " ] || [ -z "${mandatory_vars[$key]}" ]; then
      echo "'${key}' variable is empty, failing..."
      exit 1
  fi
done
found=false

echo "All variables are present. Continuing..."
echo "Getting sorted tags..."
tags=$(git tag -l --sort=v:refname)
if [ -n "${tags}" ] && [ "${tags}" != " " ]; then
  echo "Tags: $tags"
  found=true
else
  echo "No tags found, continuing..."
fi

new_tag=v$version$env

if [ -n "${brand}" ] && [ "${brand}" != " " ]; then
 {
   echo "Brand { $brand } provided."
   new_tag=v$version$env-$brand
   if [ "$found" = true ] ; then
   {
     echo "Fetching last tag on $brand..."
     old_tag=$( (echo "${tags}" | grep "$env" | grep -w "$brand") | tail -n 1)
     if [ -z "${old_tag}" ] || [ "${old_tag}" == " " ]; then
       echo "Could not find an existing tag on brand {$brand} and environment {$env}"
     else
       echo "Last tag on { $brand }: $old_tag"
     fi
   }
   fi
 }
else
  {
    echo "Brand not provided, new tag: $new_tag"
    if [ "$found" = true ] ; then
    {
    old_tag=$( (echo "${tags}" | grep -w "$env") | tail -n 1)
    if [[ $old_tag =~ "-" ]]; then
      old_tag=""
    fi
    }
    fi
  }
fi

if [[ $tags =~ $new_tag ]]; then
  {
    echo "Tag $new_tag already existing, a new release will not be created."
    exit 0
  }
fi

info_message=""
release_message=""

echo "Creating a new tag $new_tag..."
git tag "${new_tag}"

if [  -n "${old_tag}"  ] && [ "${old_tag}" != " "  ]; then
  {
  echo "Old tag: $old_tag - New tag: $new_tag"
  echo "Fetching commits between tags - $old_tag and $new_tag..."
  release_message=$(git log --pretty=medium "$old_tag".."$new_tag" | tr '\n' '\n')
  }
fi

release_name="Release $new_tag"
echo "Created new ${release_name}!"

{
  echo "new_tag=$new_tag"
  echo "release_name=$release_name"
}  >> "$GITHUB_OUTPUT"

if [ -n "${appVersion}" ] && [ "${appVersion}" != " " ]; then
  info_message="This release uses a published package with version $appVersion"
fi

EOF=$(dd if=/dev/urandom bs=15 count=1 status=none | base64)

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
    printf '\n Commits \n\n'
    echo "$release_message"
    printf '\n'
    echo "$EOF"
  } >> "$GITHUB_OUTPUT"
fi
