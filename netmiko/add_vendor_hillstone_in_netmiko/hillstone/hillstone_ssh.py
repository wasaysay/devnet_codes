import re
from netmiko.cisco_base_connection import CiscoSSHConnection

class HillstoneSSH(CiscoSSHConnection):
    def session_preparation(self) -> None:
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        self._test_channel_read(pattern=r"#")
        self.set_terminal_width(
            command="terminal width 511", pattern=r"terminal width 511"
        )
        self.disable_paging()
        self.set_base_prompt()
    # The prompt_terminator is '#'
    def set_base_prompt(self, pri_prompt_terminator=r'#',
                        alt_prompt_terminator=r'#',
                        delay_factor=0.1) -> str:
        return super(HillstoneSSH, self).set_base_prompt(pri_prompt_terminator=pri_prompt_terminator,
                                                         alt_prompt_terminator=alt_prompt_terminator,
                                                         delay_factor=delay_factor)

    def normalize_linefeeds(self, a_string: str) -> str:
        """Convert '\r\n' or '\r\r\n' to '\n, and remove extra '\r's in the text."""
        newline = re.compile(r"(\r\r\n\r|\r\r\n|\r\n)")
        return newline.sub(self.RESPONSE_RETURN, a_string).replace("\r", "\n")

    def check_enable_mode(self, check_string: str = "") -> bool:
        """Check if in enable mode. Return boolean."""
        return True

    def enable(
            self,
            cmd: str = "",
            pattern: str = "",
            enable_pattern= None,
            re_flags: int = re.IGNORECASE,
    ) -> str:
        """no enable mode."""
        return ""

    def exit_enable_mode(self, exit_command: str = "") -> str:
        """no enable (privileged exec) mode."""
        return ""

    # Set the check_string to ')#'
    def check_config_mode(self, check_string: str = ")#", pattern: str = "") -> bool:
        """
        Checks if the device is in configuration mode or not.
        """
        return super().check_config_mode(check_string=check_string, pattern=pattern)

    def config_mode(
            self,
            config_command: str = "configure",
            pattern: str = "",
            re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

# Set the exit_config to 'end'
    def exit_config_mode(self, exit_config: str = "end", pattern: str = r"#.*") -> str:
        """Exit from configuration mode."""
        return super().exit_config_mode(exit_config=exit_config, pattern=pattern)


    def save_config(self) -> str:
        """
        Save Config Example in Hillstone:
        GW# save
          Save configuration, are you sure? [y]/n: y
          Backup start configuration file, are you sure? y/[n]: y

          Building configuration.
          Saving configuration is finished
        GW#
        """
        command = 'save'
        output = self.send_command(
            command_string=command,
            expect_string=r"Save configuration",
            strip_prompt=False,
            strip_command=False
        )
        output += self.send_command(
            command_string="y",
            expect_string=r"Backup start configuration file",
            strip_prompt=False,
            strip_command=False,
            normalize=False  # without Enter after command 'y'
        )
        output += self.send_command(
            command_string="y",
            expect_string=r"Saving configuration is finished",
            strip_prompt=False,
            strip_command=False,
            normalize=False  # without Enter after command 'y'
        )

        return output