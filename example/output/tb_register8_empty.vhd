--###############################
--# Project Name : 
--# File         : 
--# Author       : 
--# Description  : 
--# Modification History
--#
--###############################

library IEEE;
use IEEE.std_logic_1164.all;

entity tb_REGISTER8 is
end tb_REGISTER8;

architecture stimulus of tb_REGISTER8 is

-- COMPONENTS --
	component REGISTER8
		port(
			CK		: in	std_logic;
			CLRN		: in	std_logic;
			LOAD		: in	std_logic;
			DIN		: in	std_logic_vector(7 downto 0);
			DOUT		: out	std_logic_vector(7 downto 0)
		);
	end component;

--
-- SIGNALS --
	signal CK		: std_logic;
	signal CLRN		: std_logic;
	signal LOAD		: std_logic;
	signal DIN		: std_logic_vector(7 downto 0);
	signal DOUT		: std_logic_vector(7 downto 0);

--
	signal RUNNING	: std_logic := '1';

begin

-- PORT MAP --
	I_REGISTER8_0 : REGISTER8
		port map (
			CK		=> CK,
			CLRN		=> CLRN,
			LOAD		=> LOAD,
			DIN		=> DIN,
			DOUT		=> DOUT
		);

--
	CLOCK: process
	begin
		while (RUNNING = '1') loop
			CK <= '1';
			wait for 10 ns;
			CK <= '0';
			wait for 10 ns;
		end loop;
		wait;
	end process CLOCK;

	GO: process
	begin
		CLRN <= '0';
		wait for 1000 ns;
		CLRN <= '1';

		RUNNING <= '0';
		wait;
	end process GO;

end stimulus;
