#!/bin/bash

networksetup -getautoproxyurl Wi-Fi
sudo networksetup -setautoproxyurl Wi-Fi http://127.0.0.1:8090/proxy.pac
