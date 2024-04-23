<script setup>
import { ref, onMounted, watch } from "vue";
import { Icon } from "@iconify/vue";
import { themeChange } from "theme-change";

const chatPromptRef = ref(null);
const chatPromptSaved = ref("");
const chatPromptLoading = ref(false);
const chatPromptResult = ref(null);
const selectedResult = ref(null);
const voiceProcessLoading = ref(false);
const voiceType = ref("male");
const voiceResult = ref(null);

const btnToggleThemeRef = ref(null);
const theme = ref("light");

// mounted
onMounted(() => {
  themeChange(false);
  window.addEventListener("beforeunload", () => {
    eel.close_python();
  });
});

// function
const toggleTheme = () => {
  theme.value = theme.value === "light" ? "dark" : "light";
  btnToggleThemeRef.value.click();
};

const cleanFilename = (prompt) => {
  const words = prompt.split(/\s+/);
  const firstFiveWords = words.slice(0, 5);
  const cleanPrompt = firstFiveWords.join(" ");
  let cleanName = cleanPrompt.replace(/[^\w\s]/g, "");
  let cleanedName = cleanName.replace(/\s+/g, "_");
  return cleanedName;
};

const update_chatPromptResult = (_result) => {
  chatPromptResult.value = _result;
};

const update_voiceResult = (_result) => {
  voiceResult.value = _result;
};

const handleSubmitPrompt = () => {
  btnSubmitPrompt();
};

const btnSubmitPrompt = () => {
  const prompt = chatPromptRef.value.value;
  if (prompt) {
    chatPromptLoading.value = true;
    chatPromptSaved.value = prompt;
    eel.create_5_jokes(prompt)(update_chatPromptResult);
    chatPromptRef.value.value = "";
  }
};

const btnGenerateVoice = () => {
  if (selectedResult.value && chatPromptSaved.value) {
    voiceProcessLoading.value = true;
    eel.generate_voice(
      selectedResult.value.setup +
        " [silent] " +
        selectedResult.value.punchline,
      cleanFilename(chatPromptSaved.value) + "_" + voiceType.value,
      voiceType.value,
    )(update_voiceResult);
  }
};

const btnPlayVoice = () => {
  if (voiceResult.value) {
    eel.play_voice(voiceResult.value);
  }
};

const btnOpenFolder = () => {
  eel.open_folder();
};

const btnExit = () => {
  eel.close_python();
};

// watcher
watch(
  () => chatPromptResult.value,
  () => {
    if (chatPromptResult.value) {
      setTimeout(() => {
        chatPromptLoading.value = false;
      }, 500);
    }
  },
);

watch(
  () => selectedResult.value,
  () => {
    voiceResult.value = null;
    voiceType.value = "male";
  },
);

watch(
  () => voiceResult.value,
  () => {
    if (voiceResult.value) {
      setTimeout(() => {
        voiceProcessLoading.value = false;
      }, 500);
    }
  },
);
</script>

<template>
  <div
    class="bg-base-300 max-w-screen mx-auto hidden h-full max-h-screen min-h-[620px] w-full min-w-[400px] flex-col gap-2.5 rounded-lg p-2.5 font-sans md:flex"
  >
    <!-- BEGIN Section Header -->
    <header
      class="bg-base-100 mb-4 flex w-full items-center justify-between gap-4 rounded-lg p-2.5 shadow-md"
    >
      <div>
        <h1 class="ml-5 text-sm font-medium">
          DeepSeek Prompt 5 Jokes to Voice with Bark
        </h1>
      </div>
      <div class="flex items-center gap-4">
        <button
          ref="btnToggleThemeRef"
          type="button"
          class="hidden"
          data-toggle-theme="dark,light"
        ></button>
        <button
          @click="toggleTheme()"
          type="button"
          class="btn btn-neutral btn-square btn-sm text-neutral-content"
        >
          <Icon
            v-if="theme === 'light'"
            icon="bx:bxs-sun"
            class="swap-on"
            data-set-theme="dark"
          />
          <Icon
            v-else
            icon="bx:bxs-moon"
            class="swap-off"
            data-set-theme="light"
          />
        </button>
        <button
          type="button"
          @click="btnExit()"
          class="btn btn-error btn-square btn-sm text-white"
        >
          <Icon icon="mdi:close" />
        </button>
      </div>
    </header>
    <!-- EOL Section Header -->
    <!-- BEGIN Section Main -->
    <main class="flex h-full w-full flex-grow flex-col px-1.5">
      <div
        class="grid h-full min-h-[300px] w-full flex-grow grid-cols-2 gap-2.5 divide-x-4 divide-gray-300"
      >
        <div class="flex h-full w-full flex-col gap-2.5">
          <div class="h-full w-full flex-grow">
            <h1 class="mb-4 px-5 text-center text-xl font-bold">Jokes Maker</h1>
            <div
              v-if="chatPromptLoading"
              class="flex h-full w-full items-center justify-center font-bold"
            >
              <span class="loading loading-spinner loading-sm mr-2"></span>
              Please Wait...
            </div>
            <div
              v-else-if="chatPromptResult && chatPromptResult.length"
              class="flex h-[380px] max-h-[380px] min-h-[380px] w-full flex-col gap-2.5 overflow-y-scroll rounded-xl pb-8 pr-5"
            >
              <div
                v-for="(joke, index) in chatPromptResult"
                :key="index"
                class="grid w-full grid-cols-5 gap-2.5"
              >
                <div class="card bg-base-100 col-span-4 w-full p-2.5">
                  <table>
                    <tr>
                      <td class="font-bold">Setup</td>
                      <td class="px-1 font-bold">:</td>
                      <td class="w-full font-medium">{{ joke.setup }}</td>
                    </tr>
                    <tr>
                      <td class="font-bold">Punchline</td>
                      <td class="px-1 font-bold">:</td>
                      <td class="w-full font-medium">{{ joke.punchline }}</td>
                    </tr>
                  </table>
                </div>
                <div
                  @click="selectedResult = joke"
                  class="btn btn-info text-info-content col-span-1 font-bold"
                >
                  Next
                  <Icon
                    icon="mdi:chevron-right"
                    class="hidden text-xl lg:inline"
                  />
                </div>
              </div>
            </div>
            <div v-else class="h-full w-full text-center">
              Start by using the prompt field below
            </div>
          </div>
          <div class="divider mt-auto"></div>
          <!-- BEGIN Section Prompt -->
          <section class="w-full">
            <form
              @submit.prevent="handleSubmitPrompt"
              class="grid w-full grid-cols-4 items-center justify-center gap-2.5"
            >
              <div class="col-span-3 flex items-center justify-center">
                <input
                  ref="chatPromptRef"
                  class="textarea textarea-bordered textarea-accent w-full font-sans"
                  placeholder="Topic"
                  :disabled="chatPromptLoading"
                />
              </div>
              <div class="col-span-1 flex items-center justify-center">
                <button
                  @click="btnSubmitPrompt()"
                  type="button"
                  class="btn group flex w-full items-center rounded-full bg-black font-bold text-white shadow-md transition-all hover:bg-blue-500 hover:shadow-lg"
                  title="send"
                  :disabled="chatPromptLoading"
                >
                  <Icon icon="bxs:send" class="hidden text-xl lg:inline" />
                  Send
                </button>
              </div>
            </form>
          </section>
          <!-- EOL Section Prompt -->
        </div>

        <div class="flex h-full w-full flex-col pl-2.5">
          <div class="flex h-full w-full flex-col gap-2.5">
            <h1 class="mb-1.5 px-5 text-center text-xl font-bold">Bark AI</h1>
            <div v-if="selectedResult" class="card bg-base-100 p-5">
              <div class="mb-4">
                <table>
                  <tr>
                    <td class="font-bold">Setup</td>
                    <td class="px-1 font-bold">:</td>
                    <td class="w-full font-medium">
                      {{ selectedResult.setup }}
                    </td>
                  </tr>
                  <tr>
                    <td class="font-bold">Punchline</td>
                    <td class="px-1 font-bold">:</td>
                    <td class="w-full font-medium">
                      {{ selectedResult.punchline }}
                    </td>
                  </tr>
                </table>
              </div>
              <div class="divider"></div>
              <div
                v-if="voiceResult"
                class="border-accent/50 mb-4 rounded-lg border-4 border-dashed px-3 py-1"
              >
                {{ voiceResult }}
              </div>
              <div class="mb-4 flex items-center justify-evenly">
                <button
                  @click="btnPlayVoice()"
                  type="button"
                  class="btn btn-success text-success-content btn-wide font-bold"
                  :disabled="!voiceResult"
                >
                  <Icon
                    icon="mdi:volume-high"
                    class="hidden text-xl lg:inline"
                  />
                  Preview
                </button>
              </div>
              <div class="mb-2 font-bold">
                Voice Type:
                <span class="font-bold uppercase">{{ voiceType }}</span>
              </div>
              <div class="flex gap-2.5">
                <button
                  @click="voiceType = 'male'"
                  type="button"
                  class="btn w-30 font-bold"
                  :class="
                    voiceType == 'male'
                      ? 'btn-active'
                      : 'btn-neutral text-neutral-content'
                  "
                >
                  <Icon icon="mdi:face-man-profile" class="hidden lg:inline" />
                  Male
                </button>
                <button
                  @click="voiceType = 'female'"
                  type="button"
                  class="btn w-30 font-bold"
                  :class="
                    voiceType == 'female'
                      ? 'btn-active'
                      : 'btn-neutral text-neutral-content'
                  "
                >
                  <Icon
                    icon="mdi:face-woman-profile"
                    class="hidden lg:inline"
                  />
                  Female
                </button>
                <button
                  @click="btnGenerateVoice()"
                  type="button"
                  class="btn btn-wide btn-accent text-accent-content ml-auto font-bold"
                >
                  <Icon
                    icon="mdi:lightning-bolt"
                    class="hidden text-xl lg:inline"
                  />
                  Generate
                </button>
              </div>
            </div>
            <div
              v-else
              class="flex h-full w-full items-center justify-center text-center"
            >
              No Data, please use the prompt field
            </div>
          </div>
          <div class="divider mt-auto"></div>
          <!-- BEGIN Section Button -->
          <section class="w-full">
            <div class="flex w-full items-center justify-evenly gap-2.5 pb-2.5">
              <button
                @click="btnOpenFolder()"
                type="button"
                class="btn btn-info text-info-content font-bold uppercase shadow-md hover:shadow-lg"
                title="send"
              >
                <Icon icon="bxs:folder" class="hidden text-xl lg:inline" />
                Open Folder
              </button>
            </div>
          </section>
          <!-- EOL Section Button -->
        </div>
      </div>
    </main>
    <!-- EOL Section Main -->
  </div>
  <div class="flex items-center justify-center p-5 text-center md:hidden">
    Screen is too small.
  </div>
  <div
    v-if="voiceProcessLoading"
    class="absolute inset-0 flex h-full w-full items-center justify-center bg-black/[.98]"
  >
    <div class="text-center text-white">
      <div class="mb-2 text-4xl font-bold tracking-widest">
        <span class="loading loading-dots loading-lg"></span>
        Processing Bark AI Voice...
      </div>
      <p class="text-xl tracking-wide">
        Depending on your hardware, this may take some time.
      </p>
    </div>
  </div>
</template>
