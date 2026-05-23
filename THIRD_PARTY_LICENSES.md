# Third-Party License Inventory

Status: preliminary internal check, not legal advice.

The current package candidate declares no runtime dependencies in
`requirements.txt` and vendors no third-party code.

| Dependency | Scope | Runtime required | License status |
|---|---:|---:|---|
| arc-agi==0.9.8 | optional repo dependency | no | requires review before runtime packaging |
| pytest>=8.0.0 | test dependency | no | not runtime required |
| jsonschema>=4.0.0 | test dependency | no | not runtime required |

Re-run this inventory after adding the real submission agent or any runtime
package modules.
