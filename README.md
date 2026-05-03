# Cross-Border Gateways and Relays

A Stellaris mod that allows empires to construct Hyper Relays and Gateways inside allied territory — including subjects, overlords, federation members, and empires linked by diplomatic pacts or guarantees.

## What This Mod Does (Technically)

Vanilla Stellaris restricts megastructure construction to systems inside the builder's own borders or those of their subjects. This is enforced in the `possible` blocks of `common/megastructures/*.txt` via triggers like `is_inside_border = from` and survey requirements.

This mod overrides two vanilla megastructure entries:

- **`hyper_relay`** — overridden in `z_ally_hyper_relay.txt`
- **`gateway_0`** — overridden in `z_ally_gateway.txt`

For each, the mod relaxes the `possible` block while preserving all vanilla prerequisites (technology, resources, starbase presence, etc.). Specifically, it adds an `OR` branch that bypasses the border and survey checks when the system's owner qualifies as an **ally** relative to the builder.

The ally logic is centralized in a single scripted trigger:

```
is_hyper_relay_ally = {
    OR = {
        is_same_value = from
        is_overlord_to = from
        is_subject = yes  (with overlord = from)
        is_in_federation_with = from
        has_non_aggression_pact = from
        has_commercial_pact = from
        has_research_agreement = from
        has_diplo_migration_treaty = from
        has_defensive_pact = from
        is_guaranteeing = from
        from = { is_guaranteeing = prev }
    }
}
```

Scope: `owner` (system owner)  
From: `from` (builder country)

## Project Structure

```
cross_border_gateways_and_relays/
  cross_border_gateways_and_relays.mod    # Launcher descriptor (contains 'path' key)
  cross_border_gateways_and_relays/
    descriptor.mod                        # Inner metadata (no 'path' key)
    common/
      megastructures/
        z_ally_gateway.txt                # Overrides vanilla gateway_0 via LIOS
        z_ally_hyper_relay.txt            # Overrides vanilla hyper_relay via LIOS
      scripted_triggers/
        ally_hyper_relay_triggers.txt     # is_hyper_relay_ally definition
```

File names in `common/megastructures/` use a `z_` prefix to ensure **Last-In-Only-Served (LIOS)** loading after vanilla files such as `14_hyper_relay.txt`. The scripted trigger file has no prefix requirement because scripted triggers are merged rather than overwritten.

## Target Game Version

**v4.3***

Future minor patches should remain compatible unless Paradox renames the megastructure keys, changes the ally trigger scopes, or significantly restructures the `possible` blocks.

## Compatibility Notes

- **Safe to add mid-game** — The mod only relaxes existing restrictions; it does not add new entities or modifiers.
- **Load order** — Place below any other mods that modify `hyper_relay` or `gateway_0` if you want this mod's ally logic to take priority. Because it uses LIOS with a `z_` prefix, it will naturally load late.
- **Conflicts** — Any mod that overwrites the same megastructure keys (`hyper_relay`, `gateway_0`) will conflict. If you use multiple gateway or relay overhaul mods, verify that only one mod is defining the `possible` block for each structure.

## Installation (Development)

1. Copy or symlink the `cross_border_gateways_and_relays/` folder into your Stellaris user mod directory:
   ```
   %USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\
   ```
2. Ensure `cross_border_gateways_and_relays.mod` (the launcher descriptor with `path=mod/cross_border_gateways_and_relays`) exists in that same `mod/` folder.
3. Launch Stellaris via the Paradox Launcher and enable the mod.
4. Check `Documents\Paradox Interactive\Stellaris\logs\error.log` after startup for script errors.

## Thumbnail Generation

The `assets/generate_thumbnail.py` script generates a 512×512 Steam Workshop thumbnail from any input image. It resizes the image, overlays the mod title on two centered lines at the top, and applies white text with a black dropshadow for readability.

Requires [Pillow](https://pillow.readthedocs.io/):
```bash
pip install pillow
python assets/generate_thumbnail.py input_image.png output_thumbnail.png
```

## Credits

This mod was created with the help of AI: **opencode** running the **Kimi K2.6** model.

## License

This project is provided as-is for the Stellaris modding community. Feel free to fork, adapt, or incorporate into your own mods with attribution.
