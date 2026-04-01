# Message: `MaterialDesc`

### Fields:
- **name**: `str`
- **tags**: `str`
- **vertex_program**: `str`
- **fragment_program**: `str`
- **vertex_space**: `int`
- **vertex_constants**: `Constant`
- **fragment_constants**: `Constant`
- **textures**: `str`
- **samplers**: `Sampler`
- **max_page_count**: `int`
- **attributes**: `VertexAttribute`
- **program**: `str`
- **pbr_parameters**: `PbrParameters`

### Enums:
- **ConstantType**:
  - `CONSTANT_TYPE_USER = 0`
  - `CONSTANT_TYPE_VIEWPROJ = 1`
  - `CONSTANT_TYPE_WORLD = 2`
  - `CONSTANT_TYPE_TEXTURE = 3`
  - `CONSTANT_TYPE_VIEW = 4`
  - `CONSTANT_TYPE_PROJECTION = 5`
  - `CONSTANT_TYPE_NORMAL = 6`
  - `CONSTANT_TYPE_WORLDVIEW = 7`
  - `CONSTANT_TYPE_WORLDVIEWPROJ = 8`
  - `CONSTANT_TYPE_USER_MATRIX4 = 9`
- **VertexSpace**:
  - `VERTEX_SPACE_WORLD = 0`
  - `VERTEX_SPACE_LOCAL = 1`
- **WrapMode**:
  - `WRAP_MODE_REPEAT = 0`
  - `WRAP_MODE_MIRRORED_REPEAT = 1`
  - `WRAP_MODE_CLAMP_TO_EDGE = 2`
- **FilterModeMin**:
  - `FILTER_MODE_MIN_NEAREST = 0`
  - `FILTER_MODE_MIN_LINEAR = 1`
  - `FILTER_MODE_MIN_NEAREST_MIPMAP_NEAREST = 2`
  - `FILTER_MODE_MIN_NEAREST_MIPMAP_LINEAR = 3`
  - `FILTER_MODE_MIN_LINEAR_MIPMAP_NEAREST = 4`
  - `FILTER_MODE_MIN_LINEAR_MIPMAP_LINEAR = 5`
  - `FILTER_MODE_MIN_DEFAULT = 6`
- **FilterModeMag**:
  - `FILTER_MODE_MAG_NEAREST = 0`
  - `FILTER_MODE_MAG_LINEAR = 1`
  - `FILTER_MODE_MAG_DEFAULT = 2`

---
