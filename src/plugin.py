import nitro

class Plugin:
  def __init__(self) -> None:
    self.lsp:nitro.LspClient = None # type: ignore
    
    # Plugin is initialized when user opens a file that is 'c' or 'cpp' language
    # so we start here a LSP process 
    self.start_clangd()

  def start_clangd(self):
    opts = nitro.LspOptions()
    opts.type = "process"
    opts.link = nitro.context.settings.get_plugin('Process')
    opts.target_languages = [ "c", "cpp" ]
    
    opts.arguments = [ ]
    opts.arguments.append(f"--header-insertion-decorators={int(bool(nitro.context.settings.get_plugin('HeaderInsertionDecorators')))}")
    
    header_insertion = "iwyu" if nitro.context.settings.get_plugin('HeaderInsertion') else "never"
    opts.arguments.append(f"--header-insertion={header_insertion}")

    self.lsp = nitro.context.create_lsp_client(opts)
    if self.lsp is not None:
      self.lsp.start()

  def on_setting_changed(self, key:str, old_value, new_value):
    if key.startswith("Plugins.Clangd."):
      if self.lsp is not None and self.lsp.is_running:
        self.lsp.stop()
      self.start_clangd()