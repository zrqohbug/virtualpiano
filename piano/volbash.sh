#!/bin/bash
echo "amixer sset 'Master' $1%"
cmd="amixer sset 'Master' $1%"
$cmd