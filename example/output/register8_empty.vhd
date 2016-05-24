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

entity REGISTER8 is
	port(
		CK		: in	std_logic;
		CLRN		: in	std_logic;
		LOAD		: in	std_logic;
		DIN		: in	std_logic_vector(7 downto 0);
		DOUT		: out	std_logic_vector(7 downto 0)
	);
end REGISTER8;

architecture struct of REGISTER8 is

begin

	TODO: process( CK, CLRN)
	begin
		if ( CLRN = '0') then

		elsif ( CK'event and CK = '1') then

	end process TODO;

end struct;

