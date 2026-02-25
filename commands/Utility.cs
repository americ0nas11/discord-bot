using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace botas.commands
{
    internal class Utility : BaseCommandModule
    {
        [Command("komandos")]
        public async Task Komandos(CommandContext ctx)
        {
            await ctx.Channel.SendMessageAsync("Komandų sąrašas:" +
                " .koks");
        }
    }
}
