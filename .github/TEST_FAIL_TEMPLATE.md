---
title: {{ env.TITLE }}
labels: bug
---

Tests are failing on {{ env.PLATFORM }} with Python {{ env.PYTHON }} when installing with `--pre` flag.

Please check the [CI run](https://github.com/{{ env.GITHUB_REPOSITORY }}/actions/runs/{{ env.RUN_ID }}) for details.