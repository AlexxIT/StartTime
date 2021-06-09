# StartTime for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Create Start Time sensor for [Home Assistant](https://www.home-assistant.io/).

![sensor](sensor.png)

## Installation

**Method 1.** [HACS](https://hacs.xyz/) custom repo:

> HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `AlexxIT/StartTime`, Category: Integration > Add > wait > StartTime > Install

**Method 2.** Manually copy `start_time` folder from [latest release](https://github.com/AlexxIT/StartTime/releases/latest) to `/config/custom_components` folder.

## Configuration

**Method 1.** GUI:

> Configuration > Integrations > Add Integration > **StartTime**

If the integration is not in the list, you need to clear the browser cache.

**Method 2.** YAML:

```yaml
start_time:
```

## About

Home Assistant displays initialization time in INFO logs. The component shows the same time as a sensor.

Useful for debugging performance of slow computers like Raspberry Pi.

This component does not depend on the settings of the `logger` component!

```
2020-02-24 17:13:11 INFO (MainThread) [homeassistant.bootstrap] Home Assistant initialized in 25.5s
```
