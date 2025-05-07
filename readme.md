# Scalabit Test

This is a pipeline deployment test for ScalaBit

### Running this locally
```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

### Testing
```
pytest
```

### Linting
```
flake8 tests/test_main.py
flake8 main.py
```

### Security check
```
bandit main.py
```

## Notes
* This application assumes the GITHUB_TOKEN is being store as a environment variable. Though it's only required when actually running the application.
* For this specific application it doesn't make sense to use a token as a user login would make more sense to manage accesses/permissions.
* The tests being made have the responses being mocked which also doesn't make any sense other than to make them as the excercise/test that this is.
* Flake8 is being used and bandit as well, would be interesting to add coverage to this as well or something like sonarcube
* A pre-commit yaml would be ideal to waste less time checking github and make things more solid
* Not a fan of the steps in the pipeline yml, but since i was having context/code location issues it was just an easier way to fix it this way. Will require more experience to apply best pratices.