import func


# フレーム切り替えのタイミング表示
def _on_Swap_called(f: func.Func) -> func.Hook:
    return func.Hook(
        is_target=f.name.startswith("glXSwap") or f.name.startswith("eglSwap"),
        before_run="onSwapCalled();",
        after_run="onSwapCompleted();",
    )


# 描画命令のタイミングを表示
def _on_Draw_called(f: func.Func) -> func.Hook:
    return func.Hook(
        is_target=f.name.startswith("glDraw"),
        before_run="onDrawCalled();",
        after_run="",
    )


with_sleep_hooks = func.Hooks(
    header='#include "throttling_frame_joined.cpp"',
    hook_funcs=[_on_Swap_called, _on_Draw_called],
)
