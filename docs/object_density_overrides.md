# Optional object densities

## Ready-to-run reference profile

From the LIBERO-PRO repository root, opt in to the bundled reference profile:

```bash
export LIBERO_OBJECT_DENSITY_CONFIG="$PWD/docs/reference_object_densities.json"
```

Run LIBERO-PRO normally in the same shell. Unset the variable to restore the released benchmark parameters. This profile has an entry for each of the 72 distinct non-articulated object category names in this revision. The source contains 76 decorated class definitions, but four repeat the same category name. It is an **unmeasured sensitivity-study scenario**, not a calibrated physics correction or a change to the default benchmark. Report scores using this profile separately from official scores.

The [mass audit](reference_object_density_audit.csv) lists the original and reference collision-body masses for the 65 categories with XML assets in this repository. Values inherited from LIBERO's reference profile are reused only where the collision geometry matches; appearance variants with the same geometry reuse the same effective density, while larger variants retain that density and therefore scale in mass with collision volume. The custom yellow mug originally mixes `100` and `0.1` kg/m³ collision geom densities, so its reference density was calculated from its own geometry and a nominal 250 g small-mug scenario. These **effective collision-geometry densities are not measured material densities**.

Seven category XMLs are missing from this repository revision: `cherries`, `corn`, `mayo`, `red_sticker`, `blue_red_sticker`, `red_box`, and `libero_mug_green`. Their 1000 kg/m³ entries are provisional key coverage only; no mass is claimed for them. The 65 available objects compiled in isolated MuJoCo collision-geom models under both original and reference densities. Full benchmark rollout validation remains pending.

## Custom profile

Set `LIBERO_OBJECT_DENSITY_CONFIG` to a JSON file mapping a movable object category or instance to a density in **kg/m³**:

```json
{
  "porcelain_mug": 800,
  "porcelain_mug_1": 950
}
```

```bash
export LIBERO_OBJECT_DENSITY_CONFIG=/absolute/path/object_densities.json
```

An instance entry takes priority over its category entry. Objects absent from the file retain their existing XML. The override changes only collision geoms (group 0) before the task XML is assembled and MuJoCo compiles it. MuJoCo derives mass and inertia from those geoms when no explicit mass or inertial element overrides them; the loader rejects an override on an object with either explicit setting. The option does not change visual meshes, contact geometry, friction, or fixtures.

Use the runtime object `category_name` for custom keys; it can differ from the BDDL registry spelling when a class name contains a digit (for example, `chefmate8_frypan` rather than `chefmate_8_frypan`). The bundled profile already uses the runtime keys.

The file is read once per path in each process. Record its contents and the effective compiled body masses with any results. Changing density changes task dynamics and can invalidate comparisons with previously reported benchmark scores. The values above are format examples, **not measured or recommended physical densities**.
