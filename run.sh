#!/usr/bin/env bash

# Get the working directory
export APP_ROOT="$(dirname "$($(type -p greadlink readlink | head -1) -f  "$BASH_SOURCE")")"

# Get defaults
source ${APP_ROOT}/defaults.sh

# Ensure we have the prereq settings
[[ -z ${org_name} ]] && read -t 60 -p "Organisation name: " org_name
[[ -z ${org_mngr_user} ]] && read -t 60 -p "Org manager user: " org_mngr_user
[[ -z ${org_mngr_pass} ]] && read -s -t 60 -p "Org manager password: " org_mngr_pass
echo -e "\n"
[[ -z ${team_op_user} ]] && read -t 60 -p "Team operator user: " team_op_user
[[ -z ${team_op_pass} ]] && read -s -t 60 -p "Team operator password: " team_op_pass
echo -e "\n "
[[ -z ${portfolio_name} ]] && read -t 60 -p "Portfolio_name: " portfolio_name

if [[ -z ${org_name} || -z ${org_mngr_user} || -z ${org_mngr_pass} || -z ${team_op_user} || -z ${team_op_pass} || -z ${portfolio_name} ]]; then
  echo "Missing required input"
  exit 0
fi

# Make sure variables are available to subprocesses
export org_mngr_user
export org_mngr_pass
export portfolio_name
export org_name

# Extrapolate the namespace
export NAMESPACE="${organisation}-${portfolio_name}"

bats endtoend.bats
