#!/bin/bash -e

# Eduard Generalov <eduard@generalov.net>
# designed to work with the Terraform External Data Source provider https://www.terraform.io/docs/providers/external/data_source.html
# for skeleton thanks to Irving Popovetsky <irving@popovetsky.com> 

function error_exit() {
  echo "$1" 1>&2
  exit 1
}

function check_deps() {
  test -f $(which curl) || error_exit "curl command not detected in path, please install it"
  test -f $(which jq) || error_exit "jq command not detected in path, please install it"
}

function parse_input() {
  eval "$(jq -r '@sh "export DOMAIN=\(.domain) USER=\(.user) PASSWORD=\(.password)"')"
}

create_token () {
  PAYLOAD=$(jq -cM -n --arg endpoint "${DOMAIN}" --arg user "${USER}" --arg password "${PASSWORD}" '{"endpoint":$endpoint,"expires_at":"2020-08-27","login":$user,"name":"terraform","password":$password,"scopes":{"personal_access_token[scopes][]":["api","sudo","read_user","read_repository"]}}')

  ANSWER=$(curl -sd"${PAYLOAD}" https://gitlab-create-pat.herokuapp.com/)
  RESULT=$(echo ${ANSWER} | jq -Mr .result)
  ERROR=$(echo ${ANSWER} | jq -Mr .error)
  echo ${ERROR} | grep null >/dev/null 2>&1 || echo "Recived ${ANSWER} from https://gitlab-create-pat.herokuapp.com/. Payload ${PAYLOAD}." >&2

}

function produce_output() {
  jq -n --arg token "${RESULT}" '{"token":$token}'
}

check_deps
parse_input
create_token
produce_output
