import hooks.throttling
import hooks.example_trace
from reg import reg
import func
import hooks

GL_REGGITRY = reg.Registry.from_file("./reg/gl.xml")
GLX_REGGITRY = reg.Registry.from_file("./reg/glx.xml")
EGL_REGGITRY = reg.Registry.from_file("./reg/egl.xml")

# Change the hooks to the ones you want to apply.
HOOKS = hooks.example_trace.dump_time_hooks
#HOOKS = hooks.throttling.with_sleep_hooks

GET_PROC_FUNCS = [
    "glXGetProcAddress",
    "eglGetProcAddress",
]


def main() -> None:
    def filter_by_api(api: str, version: float) -> bool:
        b = (api == "gl" and version <= 3.2) or (api == "glx") or (api == "egl")
        return b

    # Get all functions from OpenGL, GLX, and EGL.
    funcs = (
        func.filter_funcs(GL_REGGITRY, filter_by_api)
        | func.filter_funcs(GLX_REGGITRY, filter_by_api)
        | func.filter_funcs(EGL_REGGITRY, filter_by_api)
    )

    # Apply hooks to the functions and save hooked functions and their definitions.
    get_proc_funcs = [funcs[name] for name in GET_PROC_FUNCS if name in funcs]
    funcs = {name: f for name, f in funcs.items() if name not in GET_PROC_FUNCS}
    hooked_funcs: list[func.Func] = []
    hooked_func_defs: list[str] = []
    for fn in funcs.values():
        applied = HOOKS.apply(fn)
        if applied is None:
            continue
        hooked_funcs.append(fn)
        hooked_func_defs.append(applied)

    # Print headers
    print(func.header())
    print()
    print(HOOKS.header)
    print()

    # Print declarations of the original functions and initializer of the function pointers.
    print(func.setup_original_funcs(hooked_funcs + get_proc_funcs))
    print()

    # Print the definitions of the hooked functions.
    for defn in hooked_func_defs:
        print(defn)
        print()

    # Print the definitions of the get_proc_addr functions.
    for f in get_proc_funcs:
        print(func.define_get_proc_addr_func(f, hooked_funcs))
        print()

    # Print the definitions of the dlsym function.
    print(func.define_dlsym(hooked_funcs + get_proc_funcs))


if __name__ == "__main__":
    main()
