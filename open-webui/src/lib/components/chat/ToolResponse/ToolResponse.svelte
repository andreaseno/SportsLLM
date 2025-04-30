<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	const dispatch = createEventDispatcher();
	const i18n = getContext('i18n');

	import XMark from '$lib/components/icons/XMark.svelte';
	import AdvancedParams from '../Settings/Advanced/AdvancedParams.svelte';
	import Valves from '$lib/components/chat/Controls/Valves.svelte';
	import FileItem from '$lib/components/common/FileItem.svelte';
	import Collapsible from '$lib/components/common/Collapsible.svelte';

	import { user } from '$lib/stores';
	// export let models = [];
	// export let chatFiles = [];
	// export let params = {};
	// export let toolData: any = null;
	// export let history = {};

	// let showValves = false;
	
	// let jsonInput = '{"glossary":{"title":"example glossary","GlossDiv":{"title":"S","GlossList":{"GlossEntry":{"ID":"SGML","SortAs":"SGML","GlossTerm":"Standard Generalized Markup Language","Acronym":"SGML","Abbrev":"ISO 8879:1986","GlossDef":{"para":"A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso":["GML","XML"]},"GlossSee":"markup"}}}}}';
</script>

<div class=" dark:text-white">
	<div class=" flex items-center justify-between dark:text-gray-100 mb-2">
		<div class=" text-lg font-medium self-center font-primary">{$i18n.t('Tool Response')}</div>
		<!-- <button
			class="self-center"
			on:click={() => {
				dispatch('close');
			}}
		>
			<XMark className="size-3.5" />
		</button> -->
	</div>
	<div class="flex flex-col gap-4 p-4">
		
		{#if toolData}
			<div class="flex flex-col gap-2">
				<label class="text-sm font-medium">Function Call Data</label>
				<pre class="p-4 bg-gray-100 dark:bg-gray-800 rounded overflow-auto max-h-[100dvh]">
					<!-- {JSON.stringify(toolData, null, 2)} -->
					 <h4>id=132 first_name='Luka' last_name='Doncic' position='F-G' height='6-6' weight='230' jersey_number='77' college='Real Madrid' country='Slovenia' draft_year=2018.0 draft_round=1.0 draft_number=3.0 team=NBATeam(id=14, conference='West', division='Pacific', city='Los Angeles', name='Lakers', full_name='Los Angeles Lakers', abbreviation='LAL') team_id=None</h4>
				</pre>
			</div>
		{:else}
		<div class="flex flex-col gap-2">
			<label class="text-sm font-medium">No Function Call Data</label>
		</div>
		{/if}
	</div>
	<!-- {#if $user.role === 'admin' || $user?.permissions.chat?.controls}
		<div class=" dark:text-gray-200 text-sm font-primary py-0.5 px-0.5">
			{#if chatFiles.length > 0}
				<Collapsible title={$i18n.t('Files')} open={true} buttonClassName="w-full">
					<div class="flex flex-col gap-1 mt-1.5" slot="content">
						{#each chatFiles as file, fileIdx}
							<FileItem
								className="w-full"
								item={file}
								edit={true}
								url={file?.url ? file.url : null}
								name={file.name}
								type={file.type}
								size={file?.size}
								dismissible={true}
								on:dismiss={() => {
									// Remove the file from the chatFiles array

									chatFiles.splice(fileIdx, 1);
									chatFiles = chatFiles;
								}}
								on:click={() => {
									console.log(file);
								}}
							/>
						{/each}
					</div>
				</Collapsible>

				<hr class="my-2 border-gray-50 dark:border-gray-700/10" />
			{/if}

			<Collapsible bind:open={showValves} title={$i18n.t('Valves')} buttonClassName="w-full">
				<div class="text-sm" slot="content">
					<Valves show={showValves} />
				</div>
			</Collapsible>

			<hr class="my-2 border-gray-50 dark:border-gray-700/10" />

			<Collapsible title={$i18n.t('System Prompt')} open={true} buttonClassName="w-full">
				<div class="" slot="content">
					<textarea
						bind:value={params.system}
						class="w-full text-xs py-1.5 bg-transparent outline-none resize-none"
						rows="4"
						placeholder={$i18n.t('Enter system prompt')}
					/>
				</div>
			</Collapsible>

			<hr class="my-2 border-gray-50 dark:border-gray-700/10" />

			<Collapsible title={$i18n.t('Advanced Params')} open={true} buttonClassName="w-full">
				<div class="text-sm mt-1.5" slot="content">
					<div>
						<AdvancedParams admin={$user?.role === 'admin'} bind:params />
					</div>
				</div>
			</Collapsible>
		</div>
	{:else}
		<div class="text-sm dark:text-gray-300 text-center py-2 px-10">
			{$i18n.t('You do not have permission to access this feature.')}
		</div>
	{/if} -->
</div>
