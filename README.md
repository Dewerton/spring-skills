# Amplicode Spring Skills

Best skills for Spring Boot development powered by Amplicode Team.

## Installation

### Prerequisites

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI must be installed and running.

### Step 1: Add the marketplace

Run the following command inside Claude Code:

```
/plugin marketplace add https://github.com/Amplicode/spring-skills.git
```

This registers the catalog so you can browse available plugins. No plugins are installed yet.

### Step 2: Install the plugin

```
/plugin install spring-tools@amplicode-spring-skills
```

### Step 3: Activate

After installation, reload plugins to activate:

```
/reload-plugins
```

## Usage

Once installed, the plugin skills become available automatically during your Claude Code sessions for Spring Boot projects.

## Managing the plugin

Disable the plugin without uninstalling:

```
/plugin disable spring-tools@amplicode-spring-skills
```

Re-enable:

```
/plugin enable spring-tools@amplicode-spring-skills
```

Uninstall:

```
/plugin uninstall spring-tools@amplicode-spring-skills
```

Update marketplace to fetch the latest version:

```
/plugin marketplace update amplicode-spring-skills
```
