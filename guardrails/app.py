from guardrails import Guard, settings

settings.use_server = True
name_guard = Guard(name="name-case")
print("Name guard = " + str(name_guard))
validation_outcome = name_guard.validate("John doe")
print("Validation outcome = " + str(validation_outcome))
